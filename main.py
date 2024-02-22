import os
# from singletons import bot_state
# import singletons
from singletons.bot_config import FileName
from wrappers.json import read_json, update_json
from validate.google_creds import check_google_credentials
from validate.json_inputs import *
    

def main():
    check_google_credentials()
    info = read_json(FileName.INFO_JSON)
    if not is_json_passed_before(info):
        ... # check each field
        check_info_fields(info)
        check_course_details_regex(info)
        check_sections(info)
    
if __name__ == "__main__":
    main()