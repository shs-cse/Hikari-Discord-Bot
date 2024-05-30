import hikari, crescent
from bot_variables import state
from bot_variables.config import FileName, InfoField
from wrappers.jsonc import read_json, update_info_field
from wrappers.utils import FormatText
from validation.json_inputs import check_and_load_info

# def test_commands():
#     state.info = read_json(FileName.INFO_JSON)
#     bot = hikari.GatewayBot(state.info[InfoField.BOT_TOKEN], 
#                             intents=hikari.Intents.ALL)
#     client = crescent.Client(bot, 
#                              tracked_guilds=[int(state.info[InfoField.GUILD_ID])],
#                             #  default_guild=int(state.info[InfoField.GUILD_ID])
#                              )
#     client.plugins.load_folder(FileName.COMMANDS_FOLDER)
    
#     bot.run(
#         asyncio_debug=True,          # enable asyncio debug to detect blocking and slow code.
#         coroutine_tracking_depth=20, # enable coroutine tracking, makes some asyncio errors clearer.
#     )


# change name to save_button_info
def log_message_view(message: hikari.Message, button_view, *args):
    print(FormatText.success(f"Added button to post: {message.make_link(state.guild)}"))
    buttons : dict = state.info[InfoField.BUTTONS]
    update_info_field(InfoField.BUTTONS, {
        **buttons,
        str(message.id) : {
            'channel_id' : message.channel_id,
            'view_class': button_view.__class__.__name__,
            'view_args': [*args]
        }
    })
    


def main():
    # validate and update state.info
    check_and_load_info()
    # hikari + crescent -> create bot and client 
    bot = hikari.GatewayBot(state.info[InfoField.BOT_TOKEN], 
                            intents=hikari.Intents.ALL,
                            logs=None)  # turn off default logs from hikari
    this_guild_id = int(state.info[InfoField.GUILD_ID])
    client = crescent.Client(bot, 
                             default_guild=this_guild_id)
    # load commands and pluins
    client.plugins.load_folder(FileName.COMMANDS_FOLDER)
    client.plugins.load("sync")
    client.plugins.load("wrappers.utils")
    # run the bot
    bot.run(
        asyncio_debug=True,          # enable asyncio debug to detect blocking and slow code.
        coroutine_tracking_depth=20, # enable coroutine tracking, makes some asyncio errors clearer.
    )

if __name__ == "__main__":
    main()