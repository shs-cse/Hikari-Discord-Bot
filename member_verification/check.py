import hikari
from bot_variables import state
from bot_variables.config import EnrolmentSprdsht
from member_verification.faculty.check import try_faculty_verification
from member_verification.student.failure import check_if_student_id_is_already_taken
from member_verification.student.sucess import verify_student
from member_verification.response import Response, VerificationFailure
from wrappers.utils import FormatText

async def try_auto_member_verification(member: hikari.Member):
    response = await try_faculty_verification(member)
    if response.kind == Response.Kind.SUCCESSFUL:
        return response
    # TODO: try to check if used st invitation role
    # try verifying by advising discord server id
    ADVISING_DISCORD_ID_COL = EnrolmentSprdsht.StudentList.ADVISING_DISCORD_ID_COL
    if member.id in state.df_student[ADVISING_DISCORD_ID_COL]:
        student_id = state.df_student[state.df_student[ADVISING_DISCORD_ID_COL] == member.id]
        try:
            check_if_student_id_is_already_taken(member,student_id)
            return await verify_student(member, student_id)
        except VerificationFailure as failure:
            msg = f"Advising Server Verified Member {member.mention} {member.display_name} joined course server;"
            msg += f" but student id {student_id} already taken someone else."
            print(FormatText.warning(msg))
            return failure.response
    return Response(f"Auto-verification was not possible for {member.mention} {member.display_name}.")

# except Exception as error:
#     response = get_generic_error_response_while_verifying(error, check_member_verification)
#     msg = f"Faculty Verification: raised an error while trying to assgin sections to {ctx.member.display_name} {ctx.member.mention}."
#     print(FormatText.error(msg))
# await ctx.respond(**response)
    