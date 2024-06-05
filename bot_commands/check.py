import hikari, crescent
from bot_variables import state
from bot_variables.config import RolePermissions, RoleName
from sync_with_servers.usis import update_student_list
from sync_with_servers.sheets import update_routine
from member_verification.response import get_generic_error_response_while_verifying
from member_verification.faculty.check import try_faculty_verification
from member_verification.student.check import try_student_verification
from member_verification.check import try_member_auto_verification
from wrappers.utils import FormatText

plugin = crescent.Plugin[hikari.GatewayBot, None]()

reassign_group = crescent.Group("reassign", default_member_permissions=RolePermissions.BOT_ADMIN)
reassign_sections_sub_group =  reassign_group.sub_group("sections")

@plugin.include
@reassign_sections_sub_group.child
@crescent.command(name="to")
class CheckFacultySections:
    faculty : hikari.Member = crescent.option(hikari.User, name="faculty", description="must have faculty role.")
    
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(True)
        try:
            response = await try_faculty_verification(self.faculty)
        except Exception as error:
            response = get_generic_error_response_while_verifying(error, try_faculty_verification)
            msg = f"Faculty Verification: raised an error while trying to assgin sections to {self.faculty.display_name} {self.faculty.mention}."
            print(FormatText.error(msg))
        await ctx.respond(**response)


@plugin.include
@reassign_sections_sub_group.child
@crescent.command(name="to-all-faculties")
async def check_section_for_all_faculties(ctx: crescent.Context) -> None:
    await ctx.defer(True)
    update_routine()
    for member in state.guild.get_members().values():
        if member.get_top_role() != state.faculty_role:
            continue    
        try:
            await try_faculty_verification(member)
        except Exception as error:
            msg = f"Faculty Verification: raised an error while trying to assgin sections to {member.display_name} {member.mention}."
            print(FormatText.error(msg))
    await ctx.respond("Updated all faculty section roles from routine.")
    
    
    
verify_group = crescent.Group("verify", default_member_permissions=RolePermissions.BOT_ADMIN)
verify_member_sub_group = verify_group.sub_group("member")

@plugin.include
@verify_member_sub_group.child
@crescent.command(name="with-student-id")
class VerifyMemberWithStudentId:
    member : hikari.Member = crescent.option(hikari.User, description="Server member you want to verify.")
    student_id = crescent.option(int, name="student-id", description="Verify member with this student id.") # TODO: autocomplete
    
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(True)
        try:
            response = await try_student_verification(self.member, str(self.student_id))
        except Exception as error:
            response = get_generic_error_response_while_verifying(error, try_student_verification)
            print(FormatText.error(f"Student Verification: raised an error while trying to verify {self.member.mention} {self.member.display_name} for with {self.student_id}."))
        await ctx.respond(**response)
        


@plugin.include
@verify_member_sub_group.child
@crescent.command(name="with-advising-server")
class VerifyMemberWithAdvisingServer:
    member : hikari.Member = crescent.option(hikari.User, description="Server member you want to verify.")
    
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(True)
        try:
            response = await try_member_auto_verification(self.member)
        except Exception as error:
            response = get_generic_error_response_while_verifying(error, try_member_auto_verification)
            msg = f"Member Verification: raised an error while trying to verify member on join: {self.member.mention} {self.member.display_name}."
            print(FormatText.error(msg))
        await ctx.respond(**response)


@plugin.include
@verify_group.child
@crescent.command(name="all-members")
async def auto_verify_all_members(ctx: crescent.Context) -> None:
    await ctx.defer(True)
    update_student_list()
    for member in state.guild.get_members().values():
        if member.get_top_role().name in [RoleName.BOT, RoleName.BOT_ADMIN, RoleName.ADMIN]:
            continue
        try:
            await try_member_auto_verification(member)
        except Exception as error:
            msg = f"Member Verification: raised an error while trying to verify member on join: {member.mention} {member.display_name}."
            print(FormatText.error(msg))
    await ctx.respond("Verified as many members as possible.")
    
# TODO: check st, code repetition for single functions (user command, button, on join, slash command)