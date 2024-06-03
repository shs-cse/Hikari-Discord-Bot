import re
import pandas as pd
from bot_variables import state
from bot_variables.config import InfoField, EnrolmentSprdsht
from wrappers.pygs import get_sheet_data, update_sheet_values, get_sheet_by_name
from wrappers.utils import FormatText

def before(filenames : list[str]) -> None:
    print(FormatText.wait("Updating enrolment sheet from attedance sheet files..."))
    # read Enrolment sheet > USIS (before)
    range_start,range_end = EnrolmentSprdsht.UsisBefore.RANGE.split(':')
    usis_sheet = get_sheet_by_name(state.info[InfoField.ENROLMENT_SHEET_ID], 
                                   EnrolmentSprdsht.UsisBefore.TITLE)
    usis_data = usis_sheet.get_as_df(start=range_start[:-1], 
                                     end=range_end, 
                                     include_tailing_empty_rows=False)
    usis_data = usis_data.rename(columns={usis_data.columns[0]: 
                                            EnrolmentSprdsht.UsisBefore.SECTION_COL})
    # read ATTENDANCE_SHEET_i.xls
    for filename in filenames:
        usis_data = update_usis_dataframe_from_file(usis_data, filename)
    # update Enrolment sheet > USIS (before)
    end_row = str(usis_sheet.rows)
    usis_sheet.clear(start=range_start,
                     end=range_end+end_row)
    update_sheet_values({EnrolmentSprdsht.UsisBefore.RANGE+end_row :
                            usis_data.values.tolist()}, usis_sheet)
    update_student_list_and_routine()
    print(FormatText.success("Updated enrolment sheet from attedance sheet files."))
    
    
def extract_section_from_xls_file(filename:str) -> int:
    if filename[-4:].lower() != '.xls':
        msg = FormatText.error(f'File "{filename}" is not an xls file.')
        raise Exception(msg)
    print(FormatText.status(f"Attendance Sheet: {FormatText.bold(filename)}"))
    metadata = pd.read_excel(filename).iloc[0, 1]
    section_num = int(re.search(r"\nSection :  ([0-9]{2})\n", metadata)[1])
    print(FormatText.status(f"Section: {FormatText.bold(section_num)}"))
    return section_num


# TODO: change "ID" and "Name"
def extract_students_from_xls_file(filename:str) -> tuple[int,pd.DataFrame]:
    section_num = extract_section_from_xls_file(filename)
    section_students = pd.read_excel(filename, header=2)[["ID", "Name"]]
    section_students.insert(0, EnrolmentSprdsht.UsisBefore.SECTION_COL, section_num)
    print(FormatText.status(f"Student count: {FormatText.bold(section_students.shape[0])}"))
    return (section_num, section_students)


def update_usis_dataframe_from_file(usis_data: pd.DataFrame, filename: str) -> pd.DataFrame:
    section_num, section_students = extract_students_from_xls_file(filename)
    section_students.columns = usis_data.columns
    usis_data = usis_data[usis_data[EnrolmentSprdsht.UsisBefore.SECTION_COL] != section_num]
    usis_data = pd.concat([usis_data, section_students], ignore_index=True)
    usis_data = usis_data.sort_values(
        by=[EnrolmentSprdsht.UsisBefore.SECTION_COL, 
            EnrolmentSprdsht.StudentList.STUDENT_ID_COL], ignore_index=True)
    return usis_data
    
    
# TODO: why not update df_marks_section? like sync.sheets.pull?
def update_student_list_and_routine() -> None:
    enrolment_id = state.info[InfoField.ENROLMENT_SHEET_ID]
    # fetch student list
    print(FormatText.wait("Updating enrolled student list dataframe..."))
    state.df_student = get_sheet_data(enrolment_id, EnrolmentSprdsht.StudentList.TITLE)
    state.df_student = state.df_student.set_index(EnrolmentSprdsht.StudentList.STUDENT_ID_COL)
    state.df_student = state.df_student[state.df_student.index != '']
    print(FormatText.success("Updated enrolled student list dataframe."))
    # fetch routine data
    print(FormatText.wait("Updating routine dataframe..."))
    state.df_routine = get_sheet_data(enrolment_id, EnrolmentSprdsht.Routine.TITLE)
    print(FormatText.wait("Updated routine dataframe."))