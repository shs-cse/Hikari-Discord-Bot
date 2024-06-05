import os, hikari, crescent
import sync_with_servers.usis
from bot_variables import state
from bot_variables.config import FileName, RolePermissions
from wrappers.utils import FormatText

plugin = crescent.Plugin[hikari.GatewayBot, None]()

@plugin.include
@crescent.message_command(name="Update Attendance Sheet", 
                          default_member_permissions=RolePermissions.BOT_ADMIN)
async def update_attendacne_sheet(ctx: crescent.Context, message=hikari.Message):
    await ctx.defer()
    if not message.attachments:
        msg = f"No attachment found in the message: {message.make_link(state.guild)}"
        print(FormatText.error(msg))
        await ctx.respond(content=msg, ephemeral=True)
    filenames = []
    for attachment in message.attachments:
        filename = os.path.join(FileName.ATTENDANCE_FOLDER, attachment.filename)
        filenames.append(filename)
        await attachment.save(filename, force=True)
    sync_with_servers.usis.before(filenames)
    await ctx.respond(content=f"Update attendance sheet in USIS Before: {message.make_link(state.guild)}")