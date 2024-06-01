from bot_variables import state
from bot_variables.config import InfoField, EnrolmentSheet
from wrappers.utils import FormatText
from wrappers.pygs import get_sheet_by_name, get_sheet_data, update_sheet_values

def pull():
    print(FormatText.wait("Pulling data from google sheets..."))
    # fetch student list
    student_list_data = get_sheet_data(
                                state.info[InfoField.ENROLMENT_SHEET_ID], 
                                EnrolmentSheet.STUDENT_LIST_WRKSHT)
    state.df_student = student_list_data.set_index(EnrolmentSheet.STUDENT_ID_COL)
    state.df_student = state.df_student[state.df_student.index != '']
    # fetch routine data
    state.df_routine = get_sheet_data(
                                state.info[InfoField.ENROLMENT_SHEET_ID], 
                                EnrolmentSheet.ROUTINE_WRKSHT)
    # for tracking which student's mark is in which section's sheet
    state.df_marks_section = state.df_student[[EnrolmentSheet.DISCORD_ID_COL]]
    state.df_marks_section.insert(1, EnrolmentSheet.MARKS_SEC_COL, 0)  # new column
    state.df_marks_section.set_index(
        [state.df_marks_section.index, EnrolmentSheet.DISCORD_ID_COL], 
        inplace=True)
    print(FormatText.success("Pulling data from google sheets complete."))
    

def push():
    print(FormatText.wait("Pushing discord data to sheets..."))
    # clear old discord data
    discord_sheet = get_sheet_by_name(state.info[InfoField.ENROLMENT_SHEET_ID], 
                                      EnrolmentSheet.DISCORD_SHEET)
    discord_sheet.clear(EnrolmentSheet.DISCORD_SHEET_RANGE)
    # extract member roles
    # TODO: cleanup. is it necessaary?
    arr_updated = []
    for k, mem in enumerate(state.guild.get_members().values()):
        arr_updated.append([])
        mem_roles = sorted(mem.get_roles(), key=lambda r: r.name)
        everyone = mem_roles[0].name
        top_role_name = mem.get_top_role().name
        other_roles_names = ", ".join(role.name for role in mem_roles 
                                      if role.name not in [everyone, top_role_name])
        arr_updated[k] += [mem.username, str(mem.id), mem.display_name, everyone]
        arr_updated[k] += [top_role_name, other_roles_names]
    # dump discord data
    starting_cell = EnrolmentSheet.DISCORD_SHEET_RANGE.split(":")[0]
    update_sheet_values({starting_cell: arr_updated},
                        sheet_id=state.info[InfoField.ENROLMENT_SHEET_ID], 
                        sheet_name=EnrolmentSheet.DISCORD_SHEET)
    print(FormatText.success("Pushing discord data to sheets complete."))