import re, os
from bot_variables import state
from bot_variables.config import FileName, RegexPattern, InfoField
from wrappers.json import read_json, update_json, update_info_field
from wrappers.utils import FormatText

# match info file with the passed file to skip checking all the fields
def has_json_passed_before():
    if os.path.exists(FileName.PASSED_JSON):
        passed = read_json(FileName.PASSED_JSON)
        # matches all values with previously passed json (except buttons)
        if all(state.info[key] == passed[key] for key in state.info.keys() if key != InfoField.BUTTONS):
            print(FormatText.success("Check complete! Matches previously passed json."))
            update_json(state.info, FileName.PASSED_JSON)
            return True
        else: 
            # mismatch -> needs checking each field
            print(FormatText.warning("Needs checking each json input field..."))
            os.remove(FileName.INFO_JSON)
            return False
        

# check if info file contains all the fields
def check_info_fields():
    for attr, field in vars(InfoField).items():
        # skip private variables/attributes
        if attr.startswith("_"):
            continue
        # check if every fieldname exists in info
        if not field in state.info:
            msg = f'{FileName.INFO_JSON} file does not contain the field: "{field}".'
            raise KeyError(FormatText.error(msg))
    # passed all field checks
    msg = f"{FileName.INFO_JSON} file contains all the necessary field keys."
    print(FormatText.success(msg))
    

# check if info details matches proper regex
def check_regex_patterns():
    fields_and_patterns = {
        InfoField.COURSE_CODE: RegexPattern.COURSE_CODE,
        InfoField.COURSE_NAME: RegexPattern.COURSE_NAME,
        InfoField.SEMESTER: RegexPattern.SEMESTER,
        InfoField.ROUTINE_SHEET_ID: RegexPattern.GOOGLE_DRIVE_LINK_ID,
        InfoField.MARKS_FOLDER_ID: RegexPattern.GOOGLE_DRIVE_LINK_ID,
        InfoField.GUILD_ID: RegexPattern.DISCORD_ID,
        InfoField.BOT_TOKEN: RegexPattern.DISCORD_BOT_TOKEN,
    }
    # check each of the fields in a loop
    for field,pattern in fields_and_patterns.items():
        msg = f'{FileName.INFO_JSON} > "{field}": '
        value_str = str(state.info[field])
        extracted = re.search(pattern, value_str)
        if not extracted:
            msg += fr'"{value_str}" does not match expected pattern: "{pattern}".'
            raise ValueError(FormatText.error(msg))
        # update if not exact match (e.g full link -> id only)
        update_info_field(field, extracted[0])
        msg += f'{FormatText.BOLD}{extracted[0]}'
        print(FormatText.status(msg))
    # passed all regex checks
    msg = f"Course details regex checks out in {FileName.INFO_JSON} file."
    print(FormatText.success(msg))
    
    
# check number of sections and missing sections
def check_sections(num_sec, missing_secs):
    # make sure positive
    if num_sec <= 0:
        msg = "Number of sections must be positive"
        raise ValueError(FormatText.error(msg))
    # check missing sections
    if missing_secs:
        if 1 in missing_secs:
            msg = "Section 1 is used as template, can't be a missing section."
            raise ValueError(FormatText.error(msg))
        if not set(missing_secs).issubset(range(1, num_sec)): 
            msg = "Missing sections that don't exist"
            raise ValueError(FormatText.error(msg))
    # passed all checks
    msg = "Number of sections and missing sections seems ok."
    print(FormatText.success(msg))
    
    