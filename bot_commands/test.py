import hikari, crescent
from wrappers.utils import FormatText

plugin = crescent.Plugin[hikari.GatewayBot, None]()

bot_admin_group = crescent.Group("admin",
                                 default_member_permissions=hikari.Permissions.MANAGE_GUILD)

@plugin.include
@bot_admin_group.child
@crescent.command
async def ping(ctx: crescent.Context) -> None:
    await ctx.defer(True)
    import sync.usis
    sync.usis.before(["ATTENDANCE_SHEET (2).xls"])
    # from wrappers.discord import get_channel_by_name
    # from bot_variables.config import ChannelName
    # channel = get_channel_by_name(ChannelName.WELCOME)
    # invites = await plugin.app.rest.fetch_channel_invites(channel)
    # for invite in invites:
    #     if invite.max_age is None and invite.max_uses is None:
    #         print(str(invite))
    # from wrappers.discord import get_channel_by_name, get_role_by_name
    # role = get_role_by_name("faculty")
    # print(f"{role.mention} {role}")
    # channel = get_channel_by_name("faculty-chat")
    # # for id,po in channel.permission_overwrites.items():
    # #     print(id,po)
    # print(type(channel.permission_overwrites.values()), channel.permission_overwrites.values())
    # # from bot_variables import state
    # # await state.guild.create_category("TEST", position=0)
    await ctx.respond("Pong!")
    

@plugin.include
@crescent.event
async def ping_msg(event: hikari.GuildMessageCreateEvent) -> None:
    """If a non-bot user mentions your bot, respond with 'Pong!'."""

    # Do not respond to bots nor webhooks pinging us, only user accounts
    if not event.is_human:
        return

    me = plugin.app.get_me()

    if me.id in event.message.user_mentions_ids:
        await event.message.respond("Pong from plugin!")



@plugin.include
@crescent.command(name="random")
class RandomNumber:
    max = crescent.option(int)

    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.respond(self.max)
        
        
@plugin.include
@crescent.command(name="say")
class Say:
    to_say = crescent.option(str, "Make the bot say something", default="...", name="to-say")
    channel = crescent.option(hikari.GuildTextChannel, "The channel to send in", default=None)

    async def callback(self, ctx: crescent.Context) -> None:
        if self.channel is None:
            await ctx.app.rest.create_message(ctx.channel_id, self.to_say)
        else:
            await ctx.app.rest.create_message(self.channel.id, self.to_say)
        await ctx.respond("done", ephemeral=True)
        
        

@plugin.load_hook
def on_load() -> None:
    print(FormatText.success("Commands (and plugins) were loaded successfully."))

    # The model attribute is accessible once the plugin is loaded.
    # print(plugin.model)


@plugin.unload_hook
def on_unload() -> None:
    print(FormatText.warning("Commands (and plugins) were unloaded."))