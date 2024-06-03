import re, hikari
from bot_variables import state
from bot_variables.config import RegexPattern
from wrappers.utils import FormatText
from member_verification.response import build_response, VerificationFailure


async def check_if_member_is_a_faculty(member: hikari.Member):
    # may have hard-assigned faculty role
    if state.faculty_role.id in member.get_roles():
        return # fall through to next check
    if member.id in state.eee_guild.get_members():
        await member.add_role(state.faculty_role)
        return # fall through to next check    
    comment = "### Not A Faculty Member\n"
    comment += f"You neither have the {state.faculty_role.mention} role"
    comment += f" nor are you a member of the **{state.eee_guild.name}** server."
    comment += " So you can't assign sections to you."
    raise VerificationFailure(build_response(comment))
    
    
async def check_faculty_nickname_pattern(faculty: hikari.Member, extracted: str):
    if extracted:
        return extracted# fall through to next check
    # try display name from ECT-BC server
    name_in_eee_guild = state.eee_guild.get_member(faculty.id).display_name
    extracted = re.search(RegexPattern.FACULTY_NICKNAME, name_in_eee_guild)
    if extracted:
        print(FormatText.status(f"Change Nickname: {faculty.mention} {faculty.display_name} -> {name_in_eee_guild}..."))
        await faculty.edit(nickname=name_in_eee_guild)
        return extracted# fall through to next check
    comment = "### Nickname Not Set Properly\n"
    comment += f"Your nicknames for both this server and **{state.eee_guild.name}** server"
    comment += " is not set properly. It must be of the form: `[INITIAL] Your Name`."
    comment += f" Change your **{state.eee_guild.name}** server name, then try again."
    comment += " Some examples: \n```css\n"
    comment += "[SDS] Shadman Shahriar\n"
    comment += "[MFSQ] Md. Farhan Shadiq\n"
    comment += "[X01] Not Assigned Yet```"
    raise VerificationFailure(build_response(comment))