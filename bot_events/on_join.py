import hikari, crescent
from member_verification.response import get_generic_error_response_while_verifying
from member_verification.check import try_auto_member_verification
from wrappers.utils import FormatText

plugin = crescent.Plugin[hikari.GatewayBot, None]()    



@plugin.include
@crescent.event # after connecting to discord
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    try:
        await try_auto_member_verification(event.member)
    except Exception:
        print(FormatText.error(f"Member Verification: raised an error while trying to verify member on join: {event.member.mention} {event.member.display_name}."))
    
    


@plugin.include
@crescent.event # after connecting to discord
async def on_this_bot_join(event: hikari.GuildJoinEvent) -> None:
    new_guild = await event.fetch_guild()
    msg = f"Bot has joined the {FormatText.bold(new_guild.name)} server."
    print(FormatText.success(FormatText.bold(msg)))
