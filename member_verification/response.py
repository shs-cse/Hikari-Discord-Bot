import hikari, miru
# from bot_variables import state
# from bot_variables.config import EnrolmentSprdsht, ClassType
# from wrappers.utils import FormatText

class VerificationFailure(Exception):
    def __init__(self, response: dict) -> None:
        self.response = response
        

def build_response(comment: str, 
                   success_level: float = 0, # 0: fail, 0.5: warn, 1: success
                   inline_embed_fields: list[hikari.EmbedField] = None,
                   components: miru.View = None):
    if success_level >= 1:
        embed = hikari.Embed(title=":white_check_mark: Your account has been verified",
                                description=comment, color=0x43B581)
    elif success_level <= 0:
        embed = hikari.Embed(title=":x: Your account could not be verified",
                                description=comment, color=0xF04747)
    else:
        embed = hikari.Embed(title=":warning: Waiting for your response (Timer: 30 sec)",
                                description=comment, color=0xFFC72B)
    if inline_embed_fields:
        for field in inline_embed_fields:
            embed.add_field(field.name, field.value, inline=True)
    return {'embed': embed, 'components': components}


# # Case 5: passed all checks, should verify member
# async def verify_student(member: hikari.Member, student_id: int):
#     section = state.df_student.loc[student_id, EnrolmentSprdsht.StudentList.SECTION_COL]
#     student_name = state.df_student.loc[student_id, EnrolmentSprdsht.StudentList.NAME_COL]
#     student_name = student_name.title()
    
#     # set nickname
#     nick_to_set = f"[{student_id}] {student_name}"
#     await member.edit(nickname=nick_to_set[:32])
    
#     # handle section role
#     sec_roles_to_add = set(state.sec_roles[section].values())
#     existing_sec_roles = state.all_sec_roles & set(member.get_roles())
#     if not existing_sec_roles:
#         for role in sec_roles_to_add:
#             await member.add_role(role)
#     elif (len(existing_sec_roles) != 2 or # may have manually assigned roles
#           state.sec_roles[section][ClassType.THEORY] not in existing_sec_roles):
#         for role in existing_sec_roles:
#             await member.remove_role(role)
#         for role in sec_roles_to_add:
#             await member.add_role(role)

#     # add @student role
#     if state.student_role not in member.get_roles():
#         await member.add_role(state.student_role)

#     comment = f"You have been successfully verified as {student_name}"
#     comment += f" (ID: {student_id}) from section {section}."
#     comment += f" If this is not you, you may leave the server and try again."
#     response = build_response_for_students(comment, success_level=1, 
#                               inline_embed_fields=[
#                                   hikari.EmbedField(name="Student ID", value=f"{student_id}"),
#                                   hikari.EmbedField(name="Student Name", value=student_name),
#                                   hikari.EmbedField(name="Section", value=f"{section:02d}")
#                               ])
#     print(FormatText.success(f"Student Verification: {member.mention} was verified with id {student_id}."))
#     return response