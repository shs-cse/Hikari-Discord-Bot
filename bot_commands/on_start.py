import asyncio
from wrappers.utils import FormatText
import hikari, crescent

plugin = crescent.Plugin[hikari.GatewayBot, None]()

@plugin.include
@crescent.event # before connecting to discord
async def on_starting(event: hikari.StartingEvent) -> None:
    print(FormatText.wait("Bot is starting..."))
    # do stuff
    for i in range(5):
        print(FormatText.status(f"starting in {5-i} sec"))
        await asyncio.sleep(1)
    # Bot will now start
    
    


@plugin.include
@crescent.event # after connecting to discord
async def on_started(event: hikari.StartedEvent) -> None:
    print(FormatText.success(f"{FormatText.BOLD}Bot has started.{FormatText.DIM_BOLD_RESET}"))
    # await plugin.app.update_presence(status=hikari.Status.ONLINE)