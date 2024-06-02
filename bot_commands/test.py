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
    from member_verification.student import check_student
    from bot_variables import state
    member = state.guild.get_member(733029094660374612)
    student_id = "21101033"
    response = await check_student(member, student_id)
    await ctx.respond(**response)
    if view := response['components']:
        state.miru_client.start_view(view)
    # view = YesNoButtonsView(member, )
    # await ctx.respond(embed=hikari.Embed(title="Yes, or no?"),
    #                   components=view,ephemeral=True)
    # # embed = hikari.Embed(title="Example embed", description="An example hikari embed")
    # # embed.add_field("Field name", "Field content (value)")
    # # embed.set_thumbnail("https://i.imgur.com/EpuEOXC.jpg")
    # # embed.set_footer("This is the footer")
    # import miru

    # # Define a new custom View that contains 3 items
    # class BasicView(miru.View):

    #     # Define a new TextSelect menu with two options
    #     @miru.text_select(
    #         placeholder="Select me!",
    #         options=[
    #             miru.SelectOption(label="Option 1"),
    #             miru.SelectOption(label="Option 2"),
    #         ],
    #     )
    #     async def basic_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
    #         await ctx.respond(f"You've chosen {select.values[0]}!")

    #     # Define a new Button with the Style of success (Green)
    #     @miru.button(label="Click me!", style=hikari.ButtonStyle.SUCCESS)
    #     async def basic_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
    #         await ctx.respond("You clicked me!")

    #     # Define a new Button that when pressed will stop the view
    #     # & invalidate all the buttons in this view
    #     @miru.button(label="Stop me!", style=hikari.ButtonStyle.DANGER)
    #     async def stop_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
    #         self.stop()  # Called to stop the view
    # # Create a new instance of our view
    # view = BasicView()
    # await ctx.respond("Hello miru!", components=view)

    # Assign the view to the client and start it
    # state.miru_client.start_view(view)
    if not ctx._has_created_response:
        await ctx.respond("Pong",ephemeral=True)
    

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