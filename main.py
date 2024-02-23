import os
# from singletons import bot_state
# import singletons
from singletons.bot_config import FileName
from wrappers.json import read_json, update_json
from validation.google_sheets import check_google_credentials
from validation.json_inputs import *
    

def main():
    check_google_credentials()
    info = read_json(FileName.INFO_JSON)
    if not is_json_passed_before(info):
        ... # check each field
        check_info_fields(info)
        check_regex_patterns(info)
        check_sections(info[InfoField.NUM_SECTIONS], info[InfoField.MISSING_SECTIONS])
        info = check_and_update_routine_sheet(info)
    
if __name__ == "__main__":
    main()