from hikari import *
from bot_variables.state import bot


@bot.listen(GuildMessageCreateEvent)
async def ping(event) -> None:
    """If a non-bot user mentions your bot, respond with 'Pong!'."""

    # Do not respond to bots nor webhooks pinging us, only user accounts
    if not event.is_human:
        return

    me = bot.get_me()

    if me.id in event.message.user_mentions_ids:
        await event.message.respond("Pong!")
        
        
async def post_hello():
    ...