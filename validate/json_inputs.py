import os
from singletons.bot_config import FileName
from wrappers.json import read_json, update_json
from singletons import bot_state
from wrappers.utils import format_success_msg, format_warning_msg

def check_passed_json():
    # match `info.jsonc` the `passed.jsonc` file to skip checking all the fields
    if os.path.exists(FileName.PASSED_INFO):
        passed = read_json(FileName.PASSED_INFO)
        # matches all values with previously passed json (except buttons)
        if all(bot_state.info[key] == passed[key] for key in bot_state.info.keys() if key != 'buttons'):
            print(format_success_msg("Check complete! Matches previously passed json."))
            update_json(bot_state.info, FileName.PASSED_INFO)
            return True
        else: 
            # mismatch -> needs checking each field
            print(format_warning_msg("Needs checking each json input field..."))
            os.remove(FileName.COURSE_INFO)
            return False