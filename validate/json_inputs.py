import os, re
from singletons.bot_config import FileName, RegexPattern, InfoField
from wrappers.json import read_json, update_json
from wrappers.utils import format_success_msg, format_warning_msg, format_error_msg

# match info file with the passed file to skip checking all the fields
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
    
    
# check number of sections and missing sections
def check_sections(info):
    if info[InfoField.SECTION_COUNT] <= 0:
        msg = "Number of sections must be positive"
        raise ValueError(format_error_msg(msg))
    
    if missing := info[InfoField.MISSING_SECTIONS]:
        if 1 in missing:
            msg = "Section 1 is used as template, can't be a missing section."
            raise ValueError(format_error_msg(msg))
        if not set(missing).issubset(range(1, info['n_sections'])): 
            msg = "Missing sections that don't exist"
            raise ValueError(format_error_msg(msg))
    # passed all checks
    msg = "Number of sections and missing sections seems ok."
    print(format_success_msg(msg))
    

# check original routine spreadsheet id in json
def check_routine_spreadsheet(info):
    routine_file_id = info[InfoField.ROUTINE_SHEET_ID]
    # empty value
    if not routine_file_id:
        msg = 'No routine sheet was provided. '
        msg += f'Please update "{InfoField.ROUTINE_SHEET_ID}" in {FileName.INFO_JSON} file'
        raise ValueError(format_error_msg(msg))
    # does not match regex
    if not re.match(RegexPattern.GOOGLE_LINK_ID, routine_file_id):
        # not exact regex-match but pattern exists (probably link) 
        if extracted := re.search(RegexPattern.GOOGLE_LINK_ID, routine_file_id):
            # replace extracted id only
            info[InfoField.ROUTINE_SHEET_ID] = extracted[0]
            update_json(info, FileName.INFO_JSON)
            msg = f'Updated "{InfoField.ROUTINE_SHEET_ID}" field in {FileName.INFO_JSON} file with extracted sheet id.'
            print(format_warning_msg(msg))
        else:
            # no id found in input
            msg = f'"{InfoField.ROUTINE_SHEET_ID}" field in {FileName.INFO_JSON} file does not match expected pattern.'
            raise ValueError(format_error_msg(msg))
    