import hikari, crescent
import sync_with_servers.init, sync_with_servers.roles, sync_with_servers.sheets
from bot_variables import state
from wrappers.utils import FormatText
from view_components.student_verification.modal_and_button import VerificationButtonView
from view_components.faculty_verification.assign_sec_button import AssignSectionsButtonView

plugin = crescent.Plugin[hikari.GatewayBot, None]()


@plugin.include
@crescent.event # after connecting to discord
async def on_started(event: hikari.StartedEvent) -> None:
    await sync_with_servers.init.now()
    await sync_with_servers.roles.now()
    sync_with_servers.sheets.pull_from_enrolment()
    sync_with_servers.sheets.push_to_enrolment()
    await plugin.app.update_presence(status=hikari.Status.ONLINE)
    button_views = [VerificationButtonView(), AssignSectionsButtonView()]
    for button_view in button_views:
        state.miru_client.start_view(button_view, bind_to=None)
    print(FormatText.success(FormatText.bold("Bot has started.")))
    