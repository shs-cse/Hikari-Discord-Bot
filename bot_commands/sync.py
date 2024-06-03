import hikari, crescent
import sync_with_servers.sheets
from bot_variables import state
from bot_variables.config import InfoField, RolePermissions
from wrappers.pygs import get_link_from_sheet_id

plugin = crescent.Plugin[hikari.GatewayBot, None]()

bot_admin_sync_group = crescent.Group("sync", default_member_permissions=RolePermissions.BOT_ADMIN)

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