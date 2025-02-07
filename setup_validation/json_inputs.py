import re, os
from bot_variables import state
from bot_variables.config import FileName, RegexPattern, InfoField
from wrappers.jsonc import read_json, update_json, update_info_field
from wrappers.utils import FormatText
from setup_validation.google_sheets import check_google_credentials, check_spreadsheet_from_id
from setup_validation.google_sheets import check_enrolment_sheet, check_marks_groups_and_sheets

# match state.info with the valid json file to skip checking all the fields
def has_info_passed_before():
    if os.path.exists(FileName.VALID_JSON):
        passed = read_json(FileName.VALID_JSON)
        # matches all values with previously passed json (except buttons)
        if all(state.info[key] == passed[key] for key in state.info):
            print(FormatText.success("Check complete! Matches previously passed valid json."))
            update_json(state.info, FileName.VALID_JSON) # update valid json file
            return True
        else:
            # mismatch -> needs checking each field
            print(FormatText.warning("Needs checking every json input field..."))
            os.remove(FileName.VALID_JSON)
            return False
        
# check and load the json
def check_and_load_info():
    check_google_credentials()
    state.info = read_json(FileName.INFO_JSON)
    if not has_info_passed_before():
        check_info_fields()
        check_regex_patterns()
        check_sections(state.info[InfoField.NUM_SECTIONS], 
                       state.info[InfoField.MISSING_SECTIONS])
        check_marks_enabled()
        check_spreadsheet_from_id(state.info[InfoField.ROUTINE_SHEET_ID])
        check_enrolment_sheet()
        check_marks_groups_and_sheets()
        # create valid json file
        update_json(state.info, FileName.VALID_JSON)
    # TODO: pull data from sec marksheets, update df_marks_section (and update df_marks costly?)
        

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
        # InfoField.BOT_TOKEN: RegexPattern.DISCORD_BOT_TOKEN,
    }
    # check each of the fields in a loop
    for field,pattern in fields_and_patterns.items():
        msg = f'{FileName.INFO_JSON} > "{field}": '
        extracted = re.search(pattern, state.info[field])
        if not extracted:
            msg += fr'"{state.info[field]}" does not match expected pattern: "{pattern}".'
            raise ValueError(FormatText.error(msg))
        # update if not exact match (e.g full link -> id only)
        update_info_field(field, extracted[0])
        msg += FormatText.bold(extracted[0])
        print(FormatText.status(msg))
    # validated all regex checks
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
            msg = "Missing sections that don't exist."
            msg += " Keep in mind, the last section cannot be missing."
            msg += " Reduce number of sections instead."
            raise ValueError(FormatText.error(msg))
    # passed all checks
    msg = "Number of sections and missing sections seems ok."
    print(FormatText.success(msg))
    

# check if marks_enabled has boolean values or not
def check_marks_enabled():
    if not isinstance(state.info[InfoField.MARKS_ENABLED], bool):
        msg = "Marks enabled must be a boolean value"
        raise TypeError(FormatText.error(msg))
    # validated marks enabled
    msg = 'enabled' if state.info[InfoField.MARKS_ENABLED] else 'disabled'
    print(FormatText.success(f"Marks spreadsheets are {msg} for all sections."))