import hikari, crescent, sync
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
    print(FormatText.success(FormatText.bold("Bot has started.")))
    # await plugin.app.update_presence(status=hikari.Status.ONLINE)
    # TODO: check if bot has MANAGE_ROLES permission
    await sync.init()