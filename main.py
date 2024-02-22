import os
from consts import FileName
from wrappers.json import read_json, update_json
from validate.google_creds import check_google_credentials
from validate.json_inputs import check_passed_json
    

def main():
    # info = read_json("info.jsonc")
    # pprint(info, sort_dicts=False)
    # update_json(info, "info.jsonc")
    check_google_credentials()
    info = read_json(FileName.COURSE_INFO)
    check_passed_json()
    
if __name__ == "__main__":
    main()