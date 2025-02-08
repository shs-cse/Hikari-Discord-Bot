import hikari
import pandas as pd
from bot_variables import state
from wrappers.pygs import get_sheet_by_name
from bot_variables.config import InfoField, MarksSprdsht, MarksField
from wrappers.utils import FormatText


class MarksError(Exception):
    pass

def check_and_sync_marks(member: hikari.Member, section: int):
    roles = set(member.get_roles())
    is_admin = {state.admin_role, state.bot_admin_role} & roles
    is_sec_faculty = (
        set(state.sec_roles[section].values()) & roles & state.all_sec_roles
    )
    if is_admin or is_sec_faculty:
        pull_section_marks(section)  # publish marks of that section
    else:
        msg = f"{member.nickname} tried to sync marks for"
        msg += f" section {section} without being the section faculty."
        print(FormatText.error(msg))
        raise MarksError(msg)


def filter_and_rename_header(sec, marks: pd.DataFrame) -> pd.DataFrame:
    print(FormatText.status("Filtering out unpublished columns..."))
    marks = marks.set_index(marks.columns[0])
    marks = marks.loc[:, marks.iloc[MarksSprdsht.SecXX.ROW_FOR_PUBLISH_STATUS] == 1]
    headers = marks.columns
    marks.columns = marks.iloc[MarksSprdsht.SecXX.ROW_FOR_THIS_COL]
    marks.iloc[MarksSprdsht.SecXX.ROW_FOR_THIS_COL] = headers
    return marks


def extract_column_info(sec: int, marks: pd.DataFrame) -> pd.DataFrame:
    print(FormatText.status("Extracting column information..."))
    col_info_index_map = {
        MarksField.ColInfoIndex.HEADER: MarksSprdsht.SecXX.ROW_FOR_THIS_COL,
        MarksField.ColInfoIndex.TOTAL: MarksSprdsht.SecXX.ROW_DATA_START,
        MarksField.ColInfoIndex.CHILDREN: MarksSprdsht.SecXX.ROW_FOR_ALL_CHILDREN,
    }
    # select relevant rows only
    col_info = marks.iloc[[*col_info_index_map.values()]]
    col_info.index = pd.Index(col_info_index_map.keys())
    return col_info


def update_marks_state(sec: int, col_info: pd.DataFrame, marks: pd.DataFrame):
    # filter out rows with empty student ids
    print(FormatText.status("Extracting student marks..."))
    marks = marks[MarksSprdsht.SecXX.ROW_DATA_START + 1 :]
    marks = marks[marks.index != ""]
    # save marks data to state
    print(FormatText.status("Saving to state variable..."))
    state.all_marks[MarksField.COLUMN_INFO][sec] = col_info
    state.df_marks_sec_lookup.loc[marks.index, :] = sec
    state.all_marks[MarksField.SCORED][sec] = marks


def pull_section_marks(sec):
    if not state.info[InfoField.MARKS_ENABLED]:
        msg = f"Marks for section {sec} can't be fetched since the feature is disabled."
        print(FormatText.error(msg))
        raise MarksError(msg)
    msg = f"Fetching marks form section {sec} marks sheet..."
    print(FormatText.warning(msg))
    sec_sheet = get_sheet_by_name(
        state.info[InfoField.MARKS_SHEET_IDS][str(sec)],
        MarksSprdsht.SecXX.TITLE.format(sec),
    )
    marks_data = sec_sheet.get_as_df(start=MarksSprdsht.SecXX.HEADER_START)
    msg = f"Extracting marks from section {sec} marks sheet..."
    print(FormatText.wait(msg))
    marks = filter_and_rename_header(sec, marks_data)
    col_info = extract_column_info(sec, marks)
    update_marks_state(sec, col_info, marks)
    ...  # TODO: Create a map to get values for each marks button
    msg = f"Extracted marks from section {sec} marks sheet successfully."
    print(FormatText.success(msg))


def format_marks(scores: pd.DataFrame, col_info: pd.DataFrame, marks_col: int) -> str:
    header = col_info[marks_col][MarksField.ColInfoIndex.HEADER]
    total = col_info[marks_col][MarksField.ColInfoIndex.TOTAL]
    score = scores[marks_col]
    msg = f"{header:}:　**{score}**"
    isnumber = lambda x: isinstance(x, (int, float, complex)) and not isinstance(
        x, bool
    )
    if isnumber(total):
        msg += f"　*(out of {total})*"
    return msg


def get_student_marks(sec: int, student_id: int, marks_col: int) -> str:
    col_info = state.all_marks[MarksField.COLUMN_INFO][sec]
    if marks_col not in col_info:
        msg = f"Column {marks_col} of marks sheet for section {sec} is probably unpublished."
        print(FormatText.error(msg))
        raise MarksError(msg)
    scores = state.all_marks[MarksField.SCORED][sec].loc[student_id]
    msg = "\n# "  # markdown header
    msg += format_marks(scores, col_info, marks_col)
    children = col_info[marks_col][MarksField.ColInfoIndex.CHILDREN]  # ''/9/'9,10'
    if children:
        children = map(int, f",{children}".split(",")[1:])
        for child_col in children:
            msg += "\n> - "  # markdown quote + bullet
            msg += format_marks(scores, col_info, child_col)
    return msg


def check_if_member_has_any_marks(member:hikari.Member):
    if not state.info[InfoField.MARKS_ENABLED]:
        msg = f"Marks for {member.nickname} can't be fetched since the feature is disabled."
        print(FormatText.error(msg))
        raise MarksError(msg)
    if state.student_role not in member.get_roles():
        msg = f"{member.nickname} is not a student, can't fetch marks."
        print(FormatText.error(msg))
        raise MarksError(msg)
    if not member.id in state.df_marks_sec_lookup.index.levels[1]:
        msg = f"{member.nickname} has student role, but not in discord database."
        print(FormatText.error(msg))
        raise MarksError(msg)


def fetch_member_marks(student: hikari.Member, marks_col: int) -> str:
    check_if_member_has_any_marks(student)
    df_looked_up_by_discord = state.df_marks_sec_lookup.xs(student.id, level=1)
    student_id = df_looked_up_by_discord.index[0]
    sec = df_looked_up_by_discord.iloc[0, 0]
    if not sec:
        msg = f"{student.nickname} has no marks mapping. Was section marks synced after enabling?"
        print(FormatText.error(msg))
        raise MarksError(msg)
    msg = f"**Marks for {student.mention}**:"
    msg += get_student_marks(sec, student_id, marks_col)
    return msg
