import re, hikari
from bot_variables import state
from bot_variables.config import RegexPattern
from wrappers.utils import FormatText
from member_verification.response import VerificationFailure
from member_verification.faculty.success import assign_faculty_section_roles
from member_verification.faculty.failure import (check_if_member_is_a_faculty, 
                                                 check_faculty_nickname_pattern)

async def check_faculty_verification(member: hikari.Member):
    # may have hard-assigned faculty role
    try:
        await check_if_member_is_a_faculty(member)
        print(FormatText.wait(f"Checking faculty {member.mention} {member.display_name}"))
        extracted_initial_ish = re.search(RegexPattern.FACULTY_NICKNAME, member.display_name)
        extracted_initial = await check_faculty_nickname_pattern(member, extracted_initial_ish)
        initial = extracted_initial.group(1)
        return await assign_faculty_section_roles(member, initial)
    except VerificationFailure as failure:
        return failure.response
    # TODO: finally print checked? but won't that override failure.response to None??
    

