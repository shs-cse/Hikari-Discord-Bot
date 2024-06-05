import hikari, crescent
from member_verification.response import get_generic_error_response_while_verifying
from member_verification.faculty.check import try_faculty_verification
from member_verification.check import try_member_auto_verification
from bot_variables.config import RolePermissions
from wrappers.utils import FormatText

plugin = crescent.Plugin[hikari.GatewayBot, None]()

@plugin.include
@crescent.user_command(name="Try to Auto-Verify Member",
                       default_member_permissions=RolePermissions.BOT_ADMIN)
async def check_member(ctx: crescent.Context, member: hikari.Member):
    await ctx.defer(True)
    try:
        response = await try_member_auto_verification(member)
    except Exception as error:
        response = get_generic_error_response_while_verifying(error, try_member_auto_verification)
        msg = f"Member Verification: raised an error while trying to verify member on join: {member.mention} {member.display_name}."
        print(FormatText.error(msg))
    await ctx.respond(**response)


@plugin.include
@crescent.user_command(name="Reassign Sections to Faculty",
                       default_member_permissions=RolePermissions.BOT_ADMIN)
async def check_faculty_sections(ctx: crescent.Context, faculty: hikari.Member):
    await ctx.defer(True)
    try:
        response = await try_faculty_verification(faculty)
    except Exception as error:
        response = get_generic_error_response_while_verifying(error, try_faculty_verification)
        msg = f"Faculty Verification: raised an error while trying to assgin sections to {faculty.display_name} {faculty.mention}."
        print(FormatText.error(msg))
    await ctx.respond(**response)

# fetch marks