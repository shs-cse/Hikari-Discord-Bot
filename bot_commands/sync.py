import hikari, crescent
import sync_with_servers.sheets
from bot_variables import state
from bot_variables.config import InfoField, RolePermissions
from wrappers.pygs import get_link_from_sheet_id
from sync_with_servers.marks import MarksError, check_and_sync_marks
from wrappers.utils import FormatText


plugin = crescent.Plugin[hikari.GatewayBot, None]()

bot_admin_sync_group = crescent.Group("sync", default_member_permissions=RolePermissions.BOT_ADMIN)
bot_admin_sync_all_sec_subgroup = bot_admin_sync_group.sub_group("all-section")
faculty_sync_group = crescent.Group("sync", default_member_permissions=RolePermissions.FACULTY)

@plugin.include
@bot_admin_sync_group.child
@crescent.command(name="enrolment")
async def sync_enrolment(ctx: crescent.Context) -> None:
    await ctx.defer(ephemeral=True)
    sync_with_servers.sheets.pull_from_enrolment()
    sync_with_servers.sheets.push_to_enrolment()
    enrolment_link = get_link_from_sheet_id(state.info[InfoField.ENROLMENT_SHEET_ID])
    msg = f"Synced [Enrolment sheet]({enrolment_link})."
    msg += " Updated student list, routine and discord list."
    await ctx.respond(msg)
    
    
@plugin.include
@bot_admin_sync_group.child
@crescent.command(name="routine")
async def sync_enrolment(ctx: crescent.Context) -> None:
    await ctx.defer(ephemeral=True)
    sync_with_servers.sheets.update_routine()
    enrolment_link = get_link_from_sheet_id(state.info[InfoField.ENROLMENT_SHEET_ID])
    msg = f"Updated routine from [Enrolment sheet]({enrolment_link})."
    await ctx.respond(msg)
    

# @bot_admin sync all section marks -> print and post error if marks not enabled, else sync marks
@plugin.include
@bot_admin_sync_all_sec_subgroup.child
@crescent.command(name="marks")
async def sync_enrolment(ctx: crescent.Context) -> None:
    await ctx.defer(ephemeral=True)
    msg = f"{ctx.member.nickname} is syncing mark for all sections..."
    print(FormatText.wait(msg))
    try:
        for sec in state.available_sections:
            check_and_sync_marks(ctx.member, sec)
            msg = f"{ctx.member.nickname} has synced mark for section {sec}."
            print(FormatText.success(msg))
        msg = f"Marks for all sections has been synced."
    except MarksError:
        msg = f"Failed to sync marks for section {sec} (and subsequent sections)."
    await ctx.respond(msg)
    
    
# @faculty sync marks -> print and post error if marks not enabled, else sync marks
@plugin.include
@faculty_sync_group.child
@crescent.command(name="marks")
class SyncSecMarks:
    section = crescent.option(int)

    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(ephemeral=True)
        msg = f"{ctx.member.nickname} is syncing mark for section {self.section}..."
        print(FormatText.wait(msg))
        try:
            check_and_sync_marks(ctx.member, self.section)
            msg = f"{ctx.member.nickname} has synced mark for section {self.section}."
            print(FormatText.success(msg))
            msg = f"Marks for section {self.section} has been synced."
        except MarksError:
            msg = f"Failed to sync marks for section {self.section}."
        await ctx.respond(msg)