import hikari, crescent
import sync_with_servers.init, sync_with_servers.roles, sync_with_servers.sheets
from bot_variables import state
from wrappers.utils import FormatText
from view_components.student_verification.modal_and_button import VerificationButtonView

plugin = crescent.Plugin[hikari.GatewayBot, None]()    



@plugin.include
@crescent.event # after connecting to discord
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    new_member = event.member
    ... # TODO: check if st invite was used
    msg = f"New member {new_member.mention} {new_member.display_name} has joined."
    print(FormatText.success(FormatText.bold(msg)))
    ... # TODO: check_new_member assign roles, check nicknames and stuff
    
    

@plugin.include
@crescent.event # after connecting to discord
async def on_this_bot_join(event: hikari.GuildJoinEvent) -> None:
    new_guild = await event.fetch_guild()
    msg = f"Bot has joined the {FormatText.bold(new_guild.name)} server."
    print(FormatText.success(FormatText.bold(msg)))
