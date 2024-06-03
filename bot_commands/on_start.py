import hikari, crescent
import sync_with_servers.init, sync_with_servers.roles, sync_with_servers.sheets
from bot_variables import state
from wrappers.utils import FormatText
from view_components.student_verification.modal_and_button import VerificationButtonView

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
    await sync_with_servers.init.now()
    await sync_with_servers.roles.now()
    sync_with_servers.sheets.pull_from_enrolment()
    sync_with_servers.sheets.push_to_enrolment()
    await plugin.app.update_presence(status=hikari.Status.ONLINE)
    student_verification_button_view = VerificationButtonView()
    state.miru_client.start_view(student_verification_button_view)
    print(FormatText.success(FormatText.bold("Bot has started.")))
    