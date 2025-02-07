import hikari
import pandas as pd
from bot_variables import state
from wrappers.pygs import get_sheet_by_name
from bot_variables.config import InfoField, MarksSprdsht, MarksField
from wrappers.utils import FormatText


class MarksError(Exception):
    pass

def extract_and_update_marks(sec, marks: pd.DataFrame):
    print(FormatText.status("Filtering out unpublished columns..."))
    marks = marks.set_index(marks.columns[0])
    marks = marks.loc[:, marks.iloc[22-2] == 1]  # TODO: config.py/ filter if B22:22 is 1
    print(FormatText.status("Extracting total possible and children columns..."))
    total_start = 100 - 4  # TODO: B100:150 config.py
    max_total = marks.iloc[total_start]
    children_cols = marks.iloc[17 - 4] # TODO: B17:17 config.py
    print(FormatText.status("Extracting student marks..."))
    marks = marks[total_start + 1 :]
    marks = marks[marks.index != ""]
    update_marks_state(sec, max_total, children_cols, marks)
    
    


def update_marks_state(sec: int, max_total: pd.DataFrame, 
                       children_cols: pd.DataFrame, marks: pd.DataFrame):
    # update df_marks_section with sec_total student ids
    print(FormatText.status("Updating student to marks section mapping..."))
    state.df_marks_sec_lookup.loc[marks.index, :] = sec
    # save marks data to state
    print(FormatText.status("TODO: Saving to state variable..."))
    state.all_marks[MarksField.TOTAL][sec] = max_total
    state.all_marks[MarksField.CHILDREN][sec] = children_cols
    state.all_marks[MarksField.SCORED][sec] = marks


# TODO: move magic strings/numbers to config.py
def pull_section_marks(sec):
    if not state.info[InfoField.MARKS_ENABLED]:
        msg = f"Marks for section {sec} was pulled even though the feature is disabled."
        print(FormatText.error(msg))
        raise MarksError(msg)

    msg = f"Fetching marks form section {sec} marks sheet..."
    print(FormatText.warning(msg))
    sec_sheet = get_sheet_by_name(
        state.info[InfoField.MARKS_SHEET_IDS][str(sec)],
        MarksSprdsht.SecXX.TITLE.format(sec),
    )
    sec_marks = sec_sheet.get_as_df(start="B3")

    msg = f"Extracting marks from section {sec} marks sheet..."
    print(FormatText.wait(msg))
    extract_and_update_marks(sec, sec_marks)
    # TODO: Create a map to get values for each marks button
    msg = f"Extracted marks from section {sec} marks sheet successfully."
    print(FormatText.success(msg))

    # TODO: Discord ID -> marks_section: state.df_marks_section.xs(755317980207775755, level='Discord ID')

        
def check_and_sync_marks(member: hikari.Member, section: int):
    roles = set(member.get_roles())
    is_admin = {state.admin_role, state.bot_admin_role} & roles
    is_sec_faculty = set(state.sec_roles[section].values()) & roles & state.all_sec_roles
    if is_admin or is_sec_faculty:
        pull_section_marks(section) # publish marks of that section
    else:
        msg = f"{member.nickname} tried to sync marks for"
        msg += f" section {section} without being the section faculty."
        print(FormatText.error(msg))
        raise MarksError(msg)