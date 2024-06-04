import hikari
from bot_variables import state
from bot_variables.config import EnrolmentSprdsht
from member_verification.response import VerificationFailure, Response
from wrappers.utils import FormatText
from view_components.student_verification.yes_no_buttons import YesNoButtonsView

# Case 0: retyped input does not match
def check_retyped_user_input(input_text:str, reinput_text:str):
    if reinput_text != input_text:
        comment = "### Inputs Don't Match\nPlease try again. Your inputs"
        comment += f" `{input_text}` and `{reinput_text}` does not match."
        print(FormatText.warning(f"Student Verification: Someone's entered input ({input_text}) doesn't match retyped input ({reinput_text})."))
        raise VerificationFailure(Response(comment))
    
# Case 1: id is not a valid student id
def check_if_input_is_a_valid_id(input_text: str, extracted: str):
    if extracted:
        return # silently fall through to next check
    comment = f"### Input is Not Valid\nPlease try again. Your input `{input_text}` is not a valid student ID."
    print(FormatText.warning(f"Student Verification: Someone's input <{input_text}> is not a valid student ID."))
    raise VerificationFailure(Response(comment))

# Case 2: id is valid but not in the sheet
def check_if_student_id_is_in_database(student_id:int):
    if student_id in state.df_student.index:
        return # silently fall through to next check
    comment = f"### ID Not in Database\n`{student_id}` is not in our database."
    comment += " Please double check your student ID and try again."
    print(FormatText.warning(f"Student Verification: Student <{student_id}> not in course enrolment."))
    raise VerificationFailure(Response(comment))
    
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
        comment = f"### ID Already Taken\n`{student_id}` is already taken by {existing_member.mention}."
        comment += " If this is your old discord account and you want to use this new one,"
        comment += " please leave the sever from your old account first."
        comment += " Then try again with your new account."
        comment += " If someone else took your ID, Please report to admins ASAP."
        print(FormatText.warning(f"Student Verification: {mem.mention} tried to take <{student_id}>; but {existing_member.mention} already took it."))
        raise VerificationFailure(Response(comment))
    

# Case 4: id is valid and in the sheet, but discord does not match with advising server acc (you sure?)
async def check_if_matches_advising_server(member:hikari.Member, student_id:int):
    ADVISING_DISCORD_ID_COL = EnrolmentSprdsht.StudentList.ADVISING_DISCORD_ID_COL
    NAME_COL = EnrolmentSprdsht.StudentList.NAME_COL
    # check advising discord id
    advising_id = state.df_student.loc[student_id, ADVISING_DISCORD_ID_COL]
    if advising_id == "": # not in our advising database
        return
    # TODO: won't work. has to supply student_id anyway
    # if advising_id == member.id: # same person, auto-verify
    #     return
    # member's account exists in enrolment sheet with a different student id (conflict_id)
    if member.id in state.df_student[ADVISING_DISCORD_ID_COL]:
        conflict_id = state.df_student[state.df_student[ADVISING_DISCORD_ID_COL] == member.id]
        conflict_name = state.df_student.loc[conflict_id, NAME_COL]
        student_name = state.df_student.loc[student_id, NAME_COL]
        comment = f"Your discord account is verified as `[{conflict_id}] {conflict_name.title()[:21]}` in the advising server."
        comment += f" However, you are trying to get verified as `[{student_id}] {student_name.title()[:21]}`."
        comment += "If you think this is an error, please contact admins with proper proof."
        print(FormatText.warning(f"Student Verification: {member.mention} tried to take <{student_id}>; but advising server points to <@{advising_id}>."))
        raise VerificationFailure(Response(comment))
    # member probably has alt account -> sure?
    else:
        comment = f"### Alt Account?\n`{student_id}` was used by account with discord account <@{advising_id}> in the advising server."
        comment += "We recommend using the same discord account for both servers."
        comment += f" Are you sure you want to use this account ({member.mention}) with student id `{student_id}` for this server?"
        print(FormatText.warning(f"Student Verification: {member.mention} tried to take <{student_id}>, alt account?"))
        raise VerificationFailure(Response(comment, kind=Response.Kind.WAITING, 
                                        components=YesNoButtonsView(member,student_id)))