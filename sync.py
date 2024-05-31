import hikari, crescent
from bot_variables.config import InfoField
from wrappers.utils import FormatText
from wrappers.utils import fetch_guild_from_id, update_guild_cache, get_channel_by_name, get_role_by_name
from bot_variables import state
from bot_variables.config import EEEGuild, ChannelName, RoleName, ClassType
from validation.discord_sec import check_discord_sec
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
        msg = "Bot was not assigned @bot role.\n  Please add"
        msg += f" @bot role to {bot_mem} before proceeding."
        msg = FormatText.error(msg)
        raise hikari.HikariError(msg)
    else:
        msg = f"Bot Role: {FormatText.bold('@bot')} has been added by admin."
        print(FormatText.status(msg))
    # list of available sections (integers)
    state.available_sections = [sec for sec in 
                                    range(1, state.info[InfoField.NUM_SECTIONS]+1)
                                    if sec not in state.info[InfoField.MISSING_SECTIONS]]
    print(FormatText.status(f"Available Sections: {FormatText.bold(state.available_sections)}"))
    # create invite link from welcome channel if not found
    if not state.info[InfoField.INVITE_LINK]:
        welcome = get_channel_by_name(ChannelName.WELCOME)
        invite = await plugin.app.rest.create_invite(welcome, max_age=0, max_uses=0)
        update_info_field(InfoField.INVITE_LINK, str(invite))
    msg = FormatText.bold(state.info[InfoField.INVITE_LINK])
    print(FormatText.status(f"Invite Link: {msg}"))
    print(FormatText.success("Syncing initialization complete."))


async def roles():
    print(FormatText.wait("Syncing roles..."))
    state.admin_role = get_role_by_name(RoleName.ADMIN)
    state.bot_admin_role = get_role_by_name(RoleName.BOT_ADMIN)
    state.faculty_role = get_role_by_name(RoleName.FACULTY)
    state.faculty_sub_roles[ClassType.THEORY] = get_role_by_name(RoleName.THEORY_FACULTY)
    state.faculty_sub_roles[ClassType.LAB] = get_role_by_name(RoleName.LAB_FACULTY)
    state.st_role = get_role_by_name(RoleName.STUDENT_TUTOR)
    state.student_role = get_role_by_name(RoleName.STUDENT)
    # TODO: check all available discord sections (except 1)
    await check_discord_sec()
    print(FormatText.success("Syncing roles complete."))
    