from bot_variables import state
from bot_variables.config import InfoField, EnrolmentSprdsht
from wrappers.utils import FormatText
from wrappers.pygs import get_sheet_by_name, update_sheet_values
from sync.usis import update_student_list_and_routine

def pull():
    print(FormatText.wait("Pulling data from google sheets..."))
    update_student_list_and_routine()
    # for tracking which student's mark is in which section's sheet
    state.df_marks_section = state.df_student[[EnrolmentSprdsht.StudentList.DISCORD_ID_COL]]
    # add a new column to track which section contains that student's marks
    state.df_marks_section.insert(1, EnrolmentSprdsht.StudentList.VIRTUAL_MARKS_SEC_COL, 0) 
    state.df_marks_section.set_index(
        [state.df_marks_section.index, EnrolmentSprdsht.StudentList.DISCORD_ID_COL], 
        inplace=True)
    print(FormatText.success("Pulling data from google sheets complete."))
    

def push():
    print(FormatText.wait("Pushing discord data to sheets..."))
    # clear old discord data
    discord_sheet = get_sheet_by_name(state.info[InfoField.ENROLMENT_SHEET_ID], 
                                      EnrolmentSprdsht.Discord.TITLE)
    discord_sheet.clear(EnrolmentSprdsht.Discord.RANGE)
    # extract member roles. not sure if needed anymore
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
    starting_cell = EnrolmentSprdsht.Discord.RANGE.split(':')[0]
    update_sheet_values({starting_cell: arr_updated},
                        sheet_id=state.info[InfoField.ENROLMENT_SHEET_ID], 
                        sheet_name=EnrolmentSprdsht.Discord.TITLE)
    print(FormatText.success("Pushing discord data to sheets complete."))