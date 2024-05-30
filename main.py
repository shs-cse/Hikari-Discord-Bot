import hikari, crescent
from bot_variables import state
from bot_variables.config import FileName, InfoField
from wrappers.jsonc import read_json
from validation.json_inputs import check_and_load_info

def test_commands():
    state.info = read_json(FileName.INFO_JSON)
    bot = hikari.GatewayBot(state.info[InfoField.BOT_TOKEN], 
                            intents=hikari.Intents.ALL)
    client = crescent.Client(bot, 
                             tracked_guilds=[int(state.info[InfoField.GUILD_ID])],
                             default_guild=int(state.info[InfoField.GUILD_ID]))
    client.plugins.load_folder(FileName.COMMANDS_FOLDER)
    
    bot.run(
        asyncio_debug=True,          # enable asyncio debug to detect blocking and slow code.
        coroutine_tracking_depth=20, # enable coroutine tracking, makes some asyncio errors clearer.
    )


def test_checks():
    ...
    


def main():
    check_and_load_info() # update state.info
    bot = hikari.GatewayBot(state.info[InfoField.BOT_TOKEN], 
                            intents=hikari.Intents.ALL)
    guild_id = int(state.info[InfoField.GUILD_ID])
    client = crescent.Client(bot, 
                             tracked_guilds=[guild_id],
                             default_guild=guild_id)
    client.plugins.load_folder(FileName.COMMANDS_FOLDER)
    bot.run(
        asyncio_debug=True,          # enable asyncio debug to detect blocking and slow code.
        coroutine_tracking_depth=20, # enable coroutine tracking, makes some asyncio errors clearer.
    )

if __name__ == "__main__":
    main()