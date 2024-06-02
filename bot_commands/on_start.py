import hikari, crescent
import sync.init, sync.roles, sync.sheets
from wrappers.utils import FormatText

plugin = crescent.Plugin[hikari.GatewayBot, None]()

@plugin.include
@crescent.event # before connecting to discord
async def on_starting(event: hikari.StartingEvent) -> None:
    print(FormatText.wait("Bot is starting..."))
    # TODO: do stuff
    # for i in range(5):
    #     print(FormatText.status(f"starting in {5-i} sec"))
    #     import asyncio
    #     await asyncio.sleep(1)
    # Bot will now start
    
    


@plugin.include
@crescent.event # after connecting to discord
async def on_started(event: hikari.StartedEvent) -> None:
    await sync.init.now()
    await sync.roles.now()
    sync.sheets.pull()
    sync.sheets.push()
    await plugin.app.update_presence(status=hikari.Status.ONLINE)
    print(FormatText.success(FormatText.bold("Bot has started.")))
    