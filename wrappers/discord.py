import hikari, crescent
from bot_variables import state
from bot_variables.config import ClassType, RoleName, ChannelName, EEEGuild
from wrappers.utils import FormatText

plugin = crescent.Plugin[hikari.GatewayBot, None]()

def get_sec_role_name(section: int, class_type: ClassType):
    return RoleName.SECTION[class_type].format(section)

def get_sec_role(section: int, class_type: ClassType):
    return get_role_by_name(get_sec_role_name(section, class_type))

def get_sec_category_name(section: int, class_type: ClassType):
    return ChannelName.SECTION[class_type].format(section)

def get_sec_category(section: int, class_type: ClassType):
    return get_channel_by_name(get_sec_category_name(section, class_type))


async def fetch_guild_from_id(guild_id: hikari.Snowflakeish) -> hikari.Guild | None:
    guild_hint = "ECT-BC" if guild_id==EEEGuild.Id else "Course"
    try:
        guild = await plugin.app.rest.fetch_guild(guild_id)
        msg = f"{guild_hint} Server: {FormatText.BOLD}{guild}{FormatText.RESET}"
        print(FormatText.status(msg))
        return guild
    except hikari.NotFoundError as error:
        bot_acc = plugin.app.get_me()
        msg = f"Could not reach the {guild_hint} server. \n  Have you added this bot"
        msg += f" ({bot_acc} {bot_acc.mention}) in the {guild_hint} server?"
        msg = FormatText.error(msg)
        raise hikari.HikariError(msg) from error
    

# cache get methods by using fetch methods occasionally
async def update_guild_cache(guild=None,members=True, roles=True, channels=True):
    if not guild:
        guild = state.guild
    print(FormatText.wait("Updating guild data cache..."))
    if members:
        await plugin.app.rest.fetch_members(guild)
    if roles:
        await plugin.app.rest.fetch_roles(guild)
    if channels:
        await plugin.app.rest.fetch_guild_channels(guild)
    print(FormatText.success(f"Cache Updated: {FormatText.bold(guild)} guild's data"))


# search in list of guild channels by name
def get_channel_by_name(name: str):
    for _, channel in state.guild.get_channels().items():
        if channel.name.lower() == name.lower():
            msg = FormatText.bold('#'+name)
            print(FormatText.status(f"Fetched Channel: {msg}"))
            return channel
        
        

# search in list of guild roles by name
def get_role_by_name(name: str):
    for _, role in state.guild.get_roles().items():
        if role.name.lower() == name.lower():
            msg = FormatText.bold('@'+name)
            print(FormatText.status(f"Fetched Role: {msg}"))
            return role

# async def fetch_member_by_id(guild: hikari.Guild, id_or_user: hikari.Snowflakeish):
#     await plugin.app.rest.fetch_member(guild, id_or_user)