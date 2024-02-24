import os
from bot_variables import state
from bot_variables.config import FileName
from wrappers.json import read_json, update_json
from validation.google_sheets import check_google_credentials
from validation.json_inputs import *

import hikari, crescent


def test_commands():
    state.info = read_json(FileName.INFO_JSON)
    bot = hikari.GatewayBot(state.info[InfoField.BOT_TOKEN], intents=hikari.Intents.ALL)
    # from slash_commands import test
    client = crescent.Client(bot, default_guild=state.info[InfoField.GUILD_ID])
    client.plugins.load_folder(FileName.COMMANDS_FOLDER)
    bot.run(
        asyncio_debug=True,             # enable asyncio debug to detect blocking and slow code.
        coroutine_tracking_depth=20,    # enable tracking of coroutines, makes some asyncio
                                        # errors clearer.
        # propagate_interrupts=True,      # Any OS interrupts get rethrown as errors.
    )


def test_checks():
    check_google_credentials()
    state.info = read_json(FileName.INFO_JSON)
    if not is_json_passed_before():
        check_info_fields()
        check_regex_patterns()
        check_sections(state.info[InfoField.NUM_SECTIONS], state.info[InfoField.MISSING_SECTIONS])
        # TODO: folder for enrolment and marks
        # TODO: check or create enrolment sheet
        check_and_routine_sheet()
        ... # TODO: check sheets and stuff
        # TODO: create passed.jsonc
    


def main():
    test_checks()

if __name__ == "__main__":
    main()