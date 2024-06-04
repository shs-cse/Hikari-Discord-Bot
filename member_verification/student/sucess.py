import hikari
from member_verification.response import Response
from bot_variables import state
from bot_variables.config import EnrolmentSprdsht, ClassType
from wrappers.utils import FormatText


async def update_student_nickname(student: hikari.Member, student_id: int, student_name: str):
    nickname_to_set = f"[{student_id}] {student_name}"
    await student.edit(nickname=nickname_to_set[:32])
    
    
async def assign_student_section_roles(student: hikari.Member, section: int):
    # add @student role
    if state.student_role not in student.get_roles():
        await student.add_role(state.student_role)
    
    # handle section role
    sec_roles_to_add = set(state.sec_roles[section].values())
    existing_sec_roles = state.all_sec_roles & set(student.get_roles())
    if not existing_sec_roles:
        for role in sec_roles_to_add:
            await student.add_role(role)
    elif (len(existing_sec_roles) != 2 or # may have manually assigned roles
          state.sec_roles[section][ClassType.THEORY] not in existing_sec_roles):
        for role in existing_sec_roles:
            await student.remove_role(role)
        for role in sec_roles_to_add:
            await student.add_role(role)
    
    

# passed all checks, should verify member
async def verify_student(student: hikari.Member, student_id: int):
    student_name = state.df_student.loc[student_id, EnrolmentSprdsht.StudentList.NAME_COL]
    student_name = student_name.title()
    section = state.df_student.loc[student_id, EnrolmentSprdsht.StudentList.SECTION_COL]

    await update_student_nickname(student, student_id, student_name)
    await assign_student_section_roles(student, section)
    # # add @student role
    # if state.student_role not in student.get_roles():
    #     await student.add_role(state.student_role)
    
    # # handle section role
    # sec_roles_to_add = set(state.sec_roles[section].values())
    # existing_sec_roles = state.all_sec_roles & set(student.get_roles())
    # if not existing_sec_roles:
    #     for role in sec_roles_to_add:
    #         await student.add_role(role)
    # elif (len(existing_sec_roles) != 2 or # may have manually assigned roles
    #       state.sec_roles[section][ClassType.THEORY] not in existing_sec_roles):
    #     for role in existing_sec_roles:
    #         await student.remove_role(role)
    #     for role in sec_roles_to_add:
    #         await student.add_role(role)

    # print information about the change
    msg = f"Student Verification: {student.mention} was verified with id"
    msg += f" {student_id} and roles: " + ','.join('@'+role.name for role in student.get_roles())
    print(FormatText.success(msg))
    comment = f"### You have been successfully verified as {student_name}"
    comment += f" (ID: {student_id}) from section {section}."
    comment += f" If this is not you, you may leave the server and try again."
    response = Response(comment, 
                        kind=Response.Kind.SUCCESSFUL, 
                        inline_embed_fields=[
                            hikari.EmbedField(name="Student ID", value=f"{student_id}"),
                            hikari.EmbedField(name="Student Name", value=student_name),
                            hikari.EmbedField(name="Section", value=f"{section:02d}")
                        ])
    return response