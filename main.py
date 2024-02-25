import os
from bot_variables import state
from bot_variables.config import FileName
from wrappers.json import read_json, update_json
from validation.google_sheets import *
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
        check_spreadsheet(state.info[InfoField.ROUTINE_SHEET_ID])
        ... # TODO: check sheets and stuff
        enrolment_sheet = check_enrolment_sheet()
        check_marks_groups(enrolment_sheet)
        # TODO: marks sheets
        for marks_group in state.info[InfoField.MARKS_GROUPS]:
            for section in marks_group:
                check_marks_sheet(section, marks_group, 
                                  state.info[InfoField.MARKS_SHEET_IDS].copy())
        # check_marks_sheets()
        # TODO: create passed.jsonc
    


def main():
    test_checks()

if __name__ == "__main__":
    main()