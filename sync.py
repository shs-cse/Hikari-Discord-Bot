import hikari, crescent
from bot_variables.config import InfoField
from wrappers.utils import FormatText, update_guild_cache, get_channel_by_name, get_role_by_name, fetch_guild_from_id
from bot_variables import state
from bot_variables.config import EEEGuild, ChannelName, RoleName
from validation.json_inputs import update_info_field

plugin = crescent.Plugin[hikari.GatewayBot, None]()

async def init():
    print(FormatText.wait("Syncing initialization..."))
    # fetch course server
    this_guild_id = int(state.info[InfoField.GUILD_ID])
    state.guild = await fetch_guild_from_id(this_guild_id)
    state.eee_guild = await fetch_guild_from_id(EEEGuild.Id)
    # update cache of list of members, roles and channels
    await update_guild_cache()
    await update_guild_cache(state.eee_guild, members=True)
    # check if bot has @bot role
    bot_mem = state.guild.get_my_member()
    if bot_mem.get_top_role().name != RoleName.BOT:
        msg = "Bot was not assigned @bot role. Please add @bot role to this bot before proceeding."
        msg = FormatText.error(msg)
        raise Exception(msg)
    else:
        msg = f"Bot Role: {FormatText.BOLD}@bot{FormatText.DIM_BOLD_RESET} has been added by admin."
        print(FormatText.status(msg))
    # TODO: check if bot has bot role
    
    # list of available sections (integers)
    state.available_sections = [sec for sec in 
                                    range(1, state.info[InfoField.NUM_SECTIONS]+1)
                                    if sec not in state.info[InfoField.MISSING_SECTIONS]]
    print(FormatText.status(f"Available Sections: {state.available_sections}"))
    
    # create invite link from welcome channel if not found
    if not state.info[InfoField.INVITE_LINK]:
        welcome = get_channel_by_name(state.guild, ChannelName.WELCOME)
        invite = await plugin.app.rest.create_invite(welcome)
        update_info_field(InfoField.INVITE_LINK, str(invite))
    print(FormatText.status(f"Invite Link: {state.info[InfoField.INVITE_LINK]}"))
    print(FormatText.success("Syncing initialization complete."))
