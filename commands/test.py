import hikari, crescent

plugin = crescent.Plugin[hikari.GatewayBot, None]()

@plugin.include
@crescent.command
async def ping(ctx: crescent.Context) -> None:
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