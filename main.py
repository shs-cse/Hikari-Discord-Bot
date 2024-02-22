import os
from singletons import bot_state
# import singletons
from singletons.bot_config import FileName
from wrappers.json import read_json, update_json
from validate.google_creds import check_google_credentials
from validate.json_inputs import check_passed_json
    

def main():
    check_google_credentials()
    bot_state.info = read_json(FileName.COURSE_INFO)
    if not check_passed_json():
        ... # check each field
    
if __name__ == "__main__":
    main()