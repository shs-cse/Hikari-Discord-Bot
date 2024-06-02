import hikari
from bot_variables import state
from bot_variables.config import EnrolmentSprdsht, ClassType
from member_verification.response import VerificationFailure, build_response
from wrappers.utils import FormatText
from view_components.student_verification_yes_no import YesNoButtonsView

# Case 0: retyped input does not match
def check_retyped_user_input(input_text:str, reinput_text:str):
    if reinput_text != input_text:
        comment = "Please try again. Your inputs"
        comment += f" `{input_text}` and `{reinput_text}` does not match."
        print(FormatText.warning(f"Student Verification: Someone's input `{input_text}` doesn't match retyped input `{reinput_text}`."))
        raise VerificationFailure(build_response(comment))
    
# Case 1: id is not a valid student id
def check_if_input_is_a_valid_id(extracted: str, input_text: str = "Your input"):
    if not extracted:
        comment = f"Please try again. `{input_text}` is not a valid student ID."
        print(FormatText.warning(f"Student Verification: Someone's input `{input_text}` doesn't match student id regex."))
        raise VerificationFailure(build_response(comment))

# Case 2: id is valid but not in the sheet
def check_if_student_id_is_in_database(student_id:int):
    if student_id not in state.df_student.index:
        comment = f"`{student_id}` is not in our database."
        comment += " Please double check your student ID and try again."
        print(FormatText.warning(f"Student Verification: Student ({student_id}) not in database."))
        raise VerificationFailure(build_response(comment))
    
# Case 3: id is valid and in the sheet, but already taken (by another student/their old id)
def check_if_student_id_is_already_taken(member: hikari.Member, student_id:int):
    existing_member: hikari.Member = None
    for _, mem in state.guild.get_members().items():
        if mem.get_top_role() == state.student_role:
            if f"[{student_id}]" in mem.display_name:
                if mem.id != member.id:
                    existing_member = mem
                    break
    if existing_member: # taken by another student -> contact admin
        comment = f"`{student_id}` is already taken by {existing_member.mention}."
        comment += " If this is your old discord account and you want to use this new one,"
        comment += " please leave the sever from your old account first."
        comment += " Then try again with your new account."
        comment += " If someone else took your ID, Please report to admins ASAP."
        print(FormatText.warning(f"Student Verification: {mem.mention} tried to take {student_id}; but {existing_member.mention} already took it."))
        raise VerificationFailure(build_response(comment))
    

# Case 4: id is valid and in the sheet, but discord does not match with advising server acc (you sure?)
def check_if_matches_advising_server(member:hikari.Member, student_id:int):
    advising_id = state.df_student.loc[student_id, 
                                       EnrolmentSprdsht.StudentList.ADVISING_DISCORD_ID_COL]
    if advising_id != "" and advising_id != member.id:
        # member's account exists in enrolment sheet with a different student id (conflict_id)
        if member.id in state.df_student[EnrolmentSprdsht.StudentList.ADVISING_DISCORD_ID_COL]:
            conflict_id = state.df_student[state.df_student[EnrolmentSprdsht.StudentList.ADVISING_DISCORD_ID_COL] == member.id]
            conflict_name = state.df_student.loc[conflict_id, EnrolmentSprdsht.StudentList.NAME_COL]
            student_name = state.df_student.loc[student_id, EnrolmentSprdsht.StudentList.NAME_COL]
            comment = f"Your discord account is verified as `[{conflict_id}] {conflict_name.title()[:21]}` in the advising server."
            comment += f" However, you are trying to get verified as `[{student_id}] {student_name.title()[:21]}`."
            comment += "If you think this is an error, please contact admins with proper proof."
            print(FormatText.warning(f"Student Verification: {member.mention} tried to take {student_id}; but advising server points to <@{advising_id}>."))
            raise VerificationFailure(build_response(comment))
        # member probably has alt account -> sure?
        else:
            comment = f"`{student_id}` was used by account with discord account <@{advising_id}> in the advising server."
            comment += "We recommend using the same discord account for both servers."
            comment += f" Are you sure you want to use this account ({member.mention}) with student id `{student_id}` for this server?"
            print(FormatText.warning(f"Student Verification: {member.mention} tried to take {student_id}, alt account?"))
            raise VerificationFailure(build_response(comment, success_level=0.5, 
                                            components=YesNoButtonsView(member,student_id)))

        
        
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
#     comment += " If this is not you, please leave the server and join again."
#     response = build_response_for_students(comment, success_level=1, 
#                               inline_embed_fields=[
#                                   hikari.EmbedField(name="Student ID", value=f"{student_id}"),
#                                   hikari.EmbedField(name="Student Name", value=student_name),
#                                   hikari.EmbedField(name="Section", value=f"{section:02d}")
#                               ])
#     print(FormatText.success(f"Student Verification: {member.mention} was verified with id {student_id}."))
#     return response