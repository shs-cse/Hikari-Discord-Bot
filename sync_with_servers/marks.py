import hikari
import pandas as pd
from bot_variables import state
from bot_variables.config import InfoField, MarksSprdsht, MarksField, MarksResponse
from wrappers.pygs import get_sheet_by_name
from wrappers.utils import FormatText


class MarksError(Exception):
    pass


def check_and_sync_marks(member: hikari.Member, section: int):
    roles = set(member.get_roles())
    is_admin = {state.admin_role, state.bot_admin_role} & roles
    is_sec_faculty = set(state.sec_roles[section].values()) & roles & state.all_sec_roles
    if is_admin or is_sec_faculty:
        pull_section_marks(section)  # publish marks of that section
    else:
        log = f"{member.nickname} tried to sync marks for"
        log += f" section {section} without being the section faculty."
        print(FormatText.error(log))
        raise MarksError(log)


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
        log = f"Marks for section {sec} can't be fetched since the feature is disabled."
        print(FormatText.error(log))
        raise MarksError(log)
    log = f"Fetching marks form section {sec} marks sheet..."
    print(FormatText.warning(log))
    sec_sheet = get_sheet_by_name(
        state.info[InfoField.MARKS_SHEET_IDS][str(sec)],
        MarksSprdsht.SecXX.TITLE.format(sec),
    )
    marks_data = sec_sheet.get_as_df(start=MarksSprdsht.SecXX.HEADER_START)
    log = f"Extracting marks from section {sec} marks sheet..."
    print(FormatText.wait(log))
    marks = filter_and_rename_header(sec, marks_data)
    col_info = extract_column_info(sec, marks)
    update_marks_state(sec, col_info, marks)
    ...  # TODO: Create a map to get values for each marks button
    log = f"Extracted marks from section {sec} marks sheet successfully."
    print(FormatText.success(log))


def get_formatted_score_line(score: pd.Series, col_info: pd.DataFrame, 
                             marks_col: int) -> str:
    header = col_info[marks_col][MarksField.ColInfoIndex.HEADER]
    total = col_info[marks_col][MarksField.ColInfoIndex.TOTAL]
    msg = MarksResponse.SCORE.format(header, score)
    isnumber = lambda x: isinstance(x, (int, float, complex)) and not isinstance(x, bool)
    if isnumber(total):
        msg += MarksResponse.OUT_OF.format(total)
    return msg


def get_assessment_marks_template(sec: int, marks_col: int) -> list:
    col_info = state.all_marks[MarksField.COLUMN_INFO][sec]
    if marks_col not in col_info:
        log = f"Column {marks_col} of marks sheet for section {sec} is probably unpublished."
        print(FormatText.error(log))
        raise MarksError(log)
    main_score = get_formatted_score_line("{}", col_info, marks_col)
    msg = MarksResponse.TITLE.format(f"section {sec}")
    msg += MarksResponse.MAIN_SCORE.format(main_score)
    children = col_info[marks_col][MarksField.ColInfoIndex.CHILDREN]  # ''/9/'9,10'
    if not children:
        return msg, marks_col
    children = list(map(int, f",{children}".split(",")[1:]))
    for child_col in children:
        child_score = get_formatted_score_line("{}", col_info, child_col)
        msg += MarksResponse.CHILD_SCORE.format(child_score)
    return msg, marks_col, *children


def fetch_assessment_marks(sec: int, marks_col: int) -> tuple[str, pd.DataFrame]:
    if sec not in state.all_marks[MarksField.COLUMN_INFO]:
        log = f"Marks for section {sec} is not available. Was section marks synced after enabling?"
        print(FormatText.error(log))
        raise MarksError(log)
    log = f"Fetching marks for section {sec} and column {marks_col}..."
    print(FormatText.wait(log))
    msg, *cols = get_assessment_marks_template(sec, marks_col)
    scores = state.all_marks[MarksField.SCORED][sec] # all students from sec
    scores = scores[list(cols)]
    log = f"Fetched marks for section {sec} and column {marks_col} successfully."
    print(FormatText.success(log))
    return msg, scores


def check_if_member_has_any_marks(member: hikari.Member):
    if not state.info[InfoField.MARKS_ENABLED]:
        log = f"Marks for {member.nickname} can't be fetched since the feature is disabled."
        print(FormatText.error(log))
        raise MarksError(log)
    if state.student_role not in member.get_roles():
        log = f"{member.nickname} is not a student, can't fetch marks."
        print(FormatText.error(log))
        raise MarksError(log)
    if not member.id in state.df_marks_sec_lookup.index.levels[1]:
        log = f"{member.nickname} has student role, but not in discord database."
        print(FormatText.error(log))
        raise MarksError(log)


def fetch_member_marks(student: hikari.Member, marks_col: int) -> str:
    check_if_member_has_any_marks(student)
    log = f"Fetching marks for {student.mention} and column {marks_col}..."
    print(FormatText.wait(log))
    df_looked_up_by_discord = state.df_marks_sec_lookup.xs(student.id, level=1)
    student_id = df_looked_up_by_discord.index[0]
    sec = df_looked_up_by_discord.iloc[0, 0]
    if not sec:
        log = f"{student.nickname} has no marks mapping. Was section marks synced after enabling?"
        print(FormatText.error(log))
        raise MarksError(log)
    msg, scores = fetch_assessment_marks(sec, marks_col)
    msg = msg.format(*scores.loc[student_id])
    log = f"Fetched marks for {student.mention} and column {marks_col} successfully."
    print(FormatText.success(log))
    return msg


# # TODO: deprecate
# def get_student_marks(sec: int, student_id: int, marks_col: int) -> str:
#     col_info = state.all_marks[MarksField.COLUMN_INFO][sec]
#     if marks_col not in col_info:
#         msg = f"Column {marks_col} of marks sheet for section {sec} is probably unpublished."
#         print(FormatText.error(msg))
#         raise MarksError(msg)
#     scores = state.all_marks[MarksField.SCORED][sec].loc[student_id]
#     main_score = get_formatted_score_line(scores[marks_col], col_info, marks_col)
#     msg = MarksResponse.MAIN_SCORE.format(main_score)
#     children = col_info[marks_col][MarksField.ColInfoIndex.CHILDREN]  # ''/9/'9,10'
#     if children:
#         children = map(int, f",{children}".split(",")[1:])
#         for child_col in children:
#             child_score = get_formatted_score_line(scores[child_col], col_info, child_col)
#             msg += MarksResponse.CHILD_SCORE.format(child_score)
#     return msg


# # TODO: deprecate
# def fetch_member_marks(student: hikari.Member, marks_col: int) -> str:
#     check_if_member_has_any_marks(student)
#     df_looked_up_by_discord = state.df_marks_sec_lookup.xs(student.id, level=1)
#     student_id = df_looked_up_by_discord.index[0]
#     sec = df_looked_up_by_discord.iloc[0, 0]
#     if not sec:
#         msg = f"{student.nickname} has no marks mapping. Was section marks synced after enabling?"
#         print(FormatText.error(msg))
#         raise MarksError(msg)
#     msg = MarksResponse.TITLE.format(student.mention)
#     msg += get_student_marks(sec, student_id, marks_col)
#     return msg