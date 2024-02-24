from os import path
from bot_variables import state
from bot_variables.config import *
from pygsheets import AuthenticationError
from wrappers.pygs import *
from wrappers.utils import FormatText, get_link_from_sheet_id
from wrappers import json


def check_google_credentials():
    if not path.exists(FileName.SHEETS_CREDENTIALS):
        msg = f'Sheets credential file "{FileName.SHEETS_CREDENTIALS}" was not found.'
        msg += ' You will need to log on by clicking on this following link' 
        msg += ' and pasting the code from browser.'
        print(FormatText.warning(msg))
    try:
        get_google_client()
        print(FormatText.success("Google authorization was successful."))
    except Exception as error:
        msg = FormatText.error("Google authorization failed!"
                               " Did you forget to provide the credentials.json file?")
        raise AuthenticationError(msg) from error
    
# check if spreadsheet file exists
def check_spreadsheet(spreadsheet_id):
    try:
        spreadsheet = get_spreadsheet(spreadsheet_id)
        print(FormatText.success(f'Fetched "{spreadsheet.title}" spreadsheet successfully.'))
        return spreadsheet
    except Exception as error:
        msg = "Could not access this sheet. Is this link correct?"
        msg += " And accessible with your GSUITE accout?\n" 
        msg += get_link_from_sheet_id(spreadsheet_id)
        raise pygs.SpreadsheetNotFound(FormatText.error(msg)) from error
    

# TODO: split into multiple function
def check_enrolment_sheet():
    # enrolment id may be empty
    if enrolment_id := state.info[InfoField.ENROLMENT_SHEET_ID]:
        enrolment_sheet = check_spreadsheet(enrolment_id)
    else:
        # enrolment id not found -> create a new sheet
        msg = f'Enrolment sheet ID is not specified {FileName.INFO_JSON} file.'
        msg += ' Creating a new spreadsheet...'
        print(FormatText.warning(msg))
        file_name = FileName.ENROLMENT_SHEET.format(
                             course_code=state.info[InfoField.COURSE_CODE],
                             semester=state.info[InfoField.SEMESTER],
                         )
        enrolment_sheet = copy_spreadsheet(TemplateLinks.ENROLMENT_SHEET, 
                                           file_name,
                                           state.info[InfoField.MARKS_FOLDER_ID])
        enrolment_id = enrolment_sheet.id
    # finally update info file
    json.update_info_field(InfoField.ENROLMENT_SHEET_ID, enrolment_sheet.id)
    # update routines and stuff (for both new and old enrolment sheet)
    update_cells_from_fields(enrolment_sheet, SheetCellToFieldDict.ENROLMENT)
    allow_access(enrolment_sheet.id, state.info[InfoField.ROUTINE_SHEET_ID])
    share_with_anyone(enrolment_sheet) # also give it some time to fetch marks groups
    return enrolment_sheet
    
    
def fetch_marks_groups(enrolment_sheet):
    print(FormatText.wait(f'Fetching "{InfoField.MARKS_GROUPS}" from spreadsheet...'))
    routine_wrksht = enrolment_sheet.worksheet_by_title(PullMarksGroupsFrom.WRKSHT)
    marks_groups = routine_wrksht.get_value(PullMarksGroupsFrom.CELL)
    marks_groups = json.loads(marks_groups)
    # check sections in range 
    available_secs = set(range(1,state.info[InfoField.NUM_SECTIONS]))
    available_secs -= set(state.info[InfoField.MISSING_SECTIONS])
    if available_secs != {sec for group in marks_groups for sec in group}:
        msg = 'Marks groups contain sections that does not exist in'
        msg += f' {routine_wrksht.url}&range={PullMarksGroupsFrom.CELL}'
        raise ValueError(FormatText.error(msg))
    # update info json
    json.update_info_field(InfoField.MARKS_GROUPS, marks_groups)
    # TODO: check marks sheets
    