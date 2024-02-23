import os
from bot_variables import state
from bot_variables.config import FileName
from wrappers.json import read_json, update_json
from validation.google_sheets import check_google_credentials
from validation.json_inputs import *

import hikari, crescent


def main():
    info = read_json(FileName.INFO_JSON)
    bot = hikari.GatewayBot(token=info[InfoField.BOT_TOKEN], intents=hikari.Intents.ALL)
    # from slash_commands import test
    client = crescent.Client(bot, default_guild=info[InfoField.GUILD_ID])
    client.plugins.load_folder(FileName.COMMANDS_FOLDER)
    bot.run(
        asyncio_debug=True,             # enable asyncio debug to detect blocking and slow code.
        coroutine_tracking_depth=20,    # enable tracking of coroutines, makes some asyncio
                                        # errors clearer.
        # propagate_interrupts=True,      # Any OS interrupts get rethrown as errors.
    )


def checks():
    check_google_credentials()
    info = read_json(FileName.INFO_JSON)
    if not is_json_passed_before(info):
        check_info_fields(info)
        check_regex_patterns(info)
        check_sections(info[InfoField.NUM_SECTIONS], info[InfoField.MISSING_SECTIONS])
        info = check_and_update_routine_sheet(info)
        ... # TODO: check sheets and stuff
    
if __name__ == "__main__":
    main()