from os import path
import re
from bot_variables.config import FileName, RegexPattern, InfoField
from wrappers.json import read_json, update_json
from wrappers.utils import format_success_msg, format_warning_msg, format_error_msg

# match info file with the passed file to skip checking all the fields
def is_json_passed_before(info):
    if path.exists(FileName.PASSED_JSON):
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
        

# check if info file contains all the fields
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
    msg = f"{FileName.INFO_JSON} file contains all the necessary field keys."
    print(format_success_msg(msg))
    

# check if info details matches proper regex
def check_regex_patterns(info):
    fields_and_patterns = {
        InfoField.COURSE_CODE: RegexPattern.COURSE_CODE,
        InfoField.COURSE_NAME: RegexPattern.COURSE_NAME,
        InfoField.SEMESTER: RegexPattern.SEMESTER,
        InfoField.GUILD_ID: RegexPattern.DISCORD_ID,
        InfoField.BOT_TOKEN: RegexPattern.DISCORD_BOT_TOKEN
    }
    # check each of the fields in a loop
    for field,pattern in fields_and_patterns.items():
        if not re.match(pattern, info[field]):
            msg = f'"{field}" in {FileName.INFO_JSON} file "{info[field]}"'
            msg += fr' does not match expected pattern: "{pattern}".'
            raise SyntaxError(format_error_msg(msg))
    # passed all regex checks
    msg = f"Course details regex checks out in {FileName.INFO_JSON} file."
    print(format_success_msg(msg))
    
    
# check number of sections and missing sections
def check_sections(num_sec, missing_secs):
    # make sure positive
    if num_sec <= 0:
        msg = "Number of sections must be positive"
        raise ValueError(format_error_msg(msg))
    # check missing sections
    if missing_secs:
        if 1 in missing_secs:
            msg = "Section 1 is used as template, can't be a missing section."
            raise ValueError(format_error_msg(msg))
        if not set(missing_secs).issubset(range(1, num_sec)): 
            msg = "Missing sections that don't exist"
            raise ValueError(format_error_msg(msg))
    # passed all checks
    msg = "Number of sections and missing sections seems ok."
    print(format_success_msg(msg))
    

# check original routine spreadsheet id in json
def check_and_update_routine_sheet(info):
    pattern = RegexPattern.GOOGLE_LINK_ID
    field_name = InfoField.ROUTINE_SHEET_ID
    routine_id = info[field_name]
    extracted = re.search(pattern, routine_id)
    # raise error if no match found
    if not extracted:
        msg = f'"{field_name}" field in {FileName.INFO_JSON} ' 
        msg += f'file does not match expected pattern: "{pattern}"'
        raise ValueError(format_error_msg(msg))
    elif routine_id != extracted[0]:
        # extracted id doesn't match routine exactly
        info = update_json_routine_sheet(info, field_name, extracted[0])
    
    # TODO: check if routine sheet is reachable
    # passed all routine tests
    msg = "Original routine spreadsheet id seems ok."
    print(format_success_msg(msg))
    return info


# replace full link with extracted id only
def update_json_routine_sheet(info, routine_field, extracted_id):
    info[routine_field] = extracted_id
    update_json(info, FileName.INFO_JSON)
    msg = f'Updated "{routine_field}" field in {FileName.INFO_JSON}' 
    msg += ' file with just the extracted sheet id.'
    print(format_warning_msg(msg))
    return info
    