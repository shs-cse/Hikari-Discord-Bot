import os, re
from singletons.bot_config import FileName, RegexPattern, InfoField
from wrappers.json import read_json, update_json
from wrappers.utils import format_success_msg, format_warning_msg, format_error_msg

# match `info.jsonc` the `passed.jsonc` file to skip checking all the fields
def is_json_passed_before(info):
    if os.path.exists(FileName.PASSED_JSON):
        passed = read_json(FileName.PASSED_JSON)
        # matches all values with previously passed json (except buttons)
        if all(info[key] == passed[key] for key in info.keys() if key != InfoField.BUTTONS):
            print(format_success_msg("Check complete! Matches previously passed json."))
            update_json(info, FileName.PASSED_JSON)
            return True
        else: 
            # mismatch -> needs checking each field
            print(format_warning_msg("Needs checking each json input field..."))
            os.remove(FileName.INFO_JSON)
            return False
        

# check if `info.jsonc` file contains all the fields
def check_info_fields(info):
    for attr, field in vars(InfoField).items():
        # skip private variables/attributes
        if attr.startswith("_"):
            continue
        # check if every fieldname exists in info
        if not field in info:
            msg = f'{FileName.INFO_JSON} file does not contain the field: "{field}".'
            raise KeyError(format_error_msg(msg))
    # passed all field checks
    msg = f"{FileName.INFO_JSON} file contains all the field."
    print(format_success_msg(msg))
    


# check if course details matches proper regex
def check_course_details_regex(info):
    field_patterns = {
        InfoField.COURSE_CODE: RegexPattern.COURSE_CODE,
        InfoField.COURSE_NAME: RegexPattern.COURSE_NAME,
        InfoField.SEMESTER: RegexPattern.SEMESTER
    }
    for field,pattern in field_patterns.items():
        if not re.match(pattern, info[field]):
            msg = f'"{field}" in {FileName.INFO_JSON} file "{info[field]}"'
            msg += fr' does not match expected pattern: "{pattern}".'
            raise SyntaxError(format_error_msg(msg))
    # passed all regex checks
    msg = f"Course details regex checks out in {FileName.INFO_JSON} file."
    print(format_success_msg(msg))