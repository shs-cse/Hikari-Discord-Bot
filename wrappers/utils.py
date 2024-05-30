import hikari, crescent
from bot_variables import state
from bot_variables.config import EEEGuild

plugin = crescent.Plugin[hikari.GatewayBot, None]()

class FormatText:
    """
    Use ANSI color codes/graphics mode to emphasize changes
    reference: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    """
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    DIM_BOLD_RESET = '\033[22m'
    ITALICS = '\033[3m'
    UNDERLINE = '\033[4m'
    
    
    # dim yellow
    def wait(text):
        return f"\n{FormatText.YELLOW}{FormatText.DIM} {text}{FormatText.RESET}"

    # cyan
    def status(text):
        return f"\n{FormatText.CYAN}\t• {text}{FormatText.RESET}"
        
    # green
    def success(text):
        return f"\n{FormatText.GREEN}✔ {text}{FormatText.RESET}"

    # yellow
    def warning(text):
        return f"\n{FormatText.YELLOW}{FormatText.BOLD}‼️ {text}{FormatText.RESET}"

    # red
    def error(text):
        return f"\n\n{FormatText.RED}{FormatText.BOLD}✘ {text}{FormatText.RESET}"
    
    # only dim text and reset
    def dim(text):
        return f"{FormatText.DIM}{text}{FormatText.DIM_BOLD_RESET}"
    
    # only bold text and reset
    def bold(text):
        return f"{FormatText.BOLD}{text}{FormatText.DIM_BOLD_RESET}"
    
    




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
        raise Exception(msg) from error
    

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
    print(FormatText.status(f"Caching {guild} guild's data done."))


def get_channel_by_name(name: str):
    for _, channel in state.guild.get_channels().items():
        if channel.name == name:
            print(FormatText.status(f"Fetched Channel: {name}"))
            return channel
        
        
def get_role_by_name(roles: list[hikari.Role], name: str):
    for role in roles:
        if role.name == name:
            print(FormatText.status(f"Fetched Role: {name}"))
            return role

# async def fetch_member_by_id(guild: hikari.Guild, id_or_user: hikari.Snowflakeish):
#     await plugin.app.rest.fetch_member(guild, id_or_user)