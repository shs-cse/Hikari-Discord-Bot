import hikari, crescent
import sync.sheets
from bot_variables import state
from bot_variables.config import InfoField
from wrappers.pygs import get_link_from_sheet_id

plugin = crescent.Plugin[hikari.GatewayBot, None]()

bot_admin_group = crescent.Group("sync",
                                 default_member_permissions=hikari.Permissions.MANAGE_GUILD)

@plugin.include
@bot_admin_group.child
@crescent.command(name="enrolment")
async def sync_enrolment(ctx: crescent.Context) -> None:
    await ctx.defer(ephemeral=True)
    sync.sheets.pull_from_enrolment()
    sync.sheets.push_to_enrolment()
    enrolment_link = get_link_from_sheet_id(state.info[InfoField.ENROLMENT_SHEET_ID])
    msg = f"Synced [Enrolment sheet]({enrolment_link})."
    msg += " Updated student list, routine and discord list."
    await ctx.respond(msg)