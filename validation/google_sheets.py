from os import path
from bot_variables import state
from bot_variables.config import FileName, InfoField
from pygsheets import AuthenticationError
from wrappers.pygs import *
from wrappers.utils import FormatText, get_link_from_sheet_id

# TODO: check routine sheet id in B16
# TODO: check enrolment sheet
# TODO: allow access routine
# TODO: fetch marks groups

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
        print(FormatText.ok("Fetching routine sheet..."))
        spreadsheet = get_spreadsheet(spreadsheet_id)
        print(FormatText.success("Fetched routine sheet."))
        return spreadsheet
    except Exception as error:
        msg = "Could not access this sheet. Is this link correct?"
        msg += " And accessible with your GSUITE accout?\n" 
        msg += get_link_from_sheet_id(spreadsheet_id)
        raise pygs.SpreadsheetNotFound(FormatText.error(msg)) from error
    

def check_enrolment():
    enrolment_id = state.info[InfoField.ENROLMENT_SHEET_ID]
    if enrolment_id:
        enrolment_sheet = check_spreadsheet(enrolment_id)
    else:
        # TODO: if not, create one
        msg = f'Enrolment sheet ID is not specified {FileName.INFO_JSON} file.'
        msg += ' Creating a new sheet...'
        print(FormatText.warning(msg))
        
    # TODO: check routine sheet is in B16
    ...