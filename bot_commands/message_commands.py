import os, hikari, crescent
import sync_with_servers.usis
from bot_variables import state
from bot_variables.config import FileName, RolePermissions, ChannelName
from wrappers.discord import get_channel_by_name
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
    
    
@plugin.include
@crescent.message_command(name="Copy this Post to General Announcement as Bot", 
                          default_member_permissions=RolePermissions.BOT_ADMIN)
async def post_to_general_announcement(ctx: crescent.Context, from_message=hikari.Message):
    await ctx.defer(True)
    general_announcement_channel = get_channel_by_name(ChannelName.GENERAL_ANNOUNCEMENT)
    new_message = await plugin.app.rest.create_message(
                            channel=general_announcement_channel,
                            content=from_message.content,
                            attachments=from_message.attachments,
                            components=from_message.components,
                            embeds=from_message.embeds,
                            stickers=from_message.stickers,
                            tts=from_message.is_tts,
                            mentions_everyone=from_message.mentions_everyone,
                            user_mentions=from_message.user_mentions_ids,
                            role_mentions=from_message.role_mention_ids)
    await ctx.respond(f"Your message has been posted to {general_announcement_channel.mention}: {new_message.make_link(state.guild)}")