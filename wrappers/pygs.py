import pygsheets.client
import requests, pygsheets, re
import pandas as pd
from pygsheets.exceptions import *
from bot_variables.config import RegexPattern
from wrappers.utils import FormatText
from bot_variables.config import FileName
from bot_variables import state

# TODO: change all sheet to either spreadsheet or worksheet to clear confusions
# TODO: check if file in trash

# folder id -> link
def get_link_from_folder_id(folder_id: str) -> str:
    return f"https://drive.google.com/drive/folders/{folder_id}"
    
# sheet id -> link
def get_link_from_sheet_id(sheet_id: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}"

# destination sheet id + source sheet id -> allow access link
def get_allow_access_link_from_sheet_id(dest_sheet_id: str, 
                                        src_sheet_id: str) -> str:
    dest_sheet_url = get_link_from_sheet_id(dest_sheet_id)
    return f"{dest_sheet_url}/externaldata/addimportrangepermissions?donorDocId={src_sheet_id}"

# link -> sheets/folder id
def get_drive_id_from_link(link: str) -> str:
    return re.search(RegexPattern.GOOGLE_DRIVE_LINK_ID, link).group()

# authorization
def get_google_client() -> pygsheets.client.Client:
    return pygsheets.authorize(client_secret = FileName.GOOGLE_CREDENTIALS)


# get a spreadsheet object
def get_spreadsheet(spreadsheet_id: str) -> pygsheets.Spreadsheet:
    print(FormatText.wait("Fetching spreadsheet..."))
    url = get_link_from_sheet_id(spreadsheet_id)
    msg = f"Url: {FormatText.bold(url)}"
    print(FormatText.status(msg))
    google_client = get_google_client()
    try:
        spreadsheet = google_client.open_by_key(spreadsheet_id)
        msg = FormatText.bold(spreadsheet.title)
        print(FormatText.success(f'Fetched "{msg}" spreadsheet successfully.'))
    except Exception as error:
        msg = "Could not access this sheet. Is this link correct?"
        msg += " And accessible with your GSUITE accout?\n" 
        msg += get_link_from_sheet_id(spreadsheet_id)
        raise SpreadsheetNotFound(FormatText.error(msg)) from error
    # warn if file is trashed
    drive_api_files = google_client.drive.service.files()
    trashed_response = drive_api_files.get(fileId=spreadsheet_id, fields='trashed').execute()
    trashed = trashed_response['trashed']
    if trashed:
        print(FormatText.warning('Fetched spreadsheet is in google drive trash!!'))
    return spreadsheet


# get a specific sheet (tab) by name from a spreadsheet
def get_sheet_by_name(spreadsheet_obj_or_id: pygsheets.Spreadsheet | str, 
                      sheet_name: str) -> pygsheets.Worksheet:
    if isinstance(spreadsheet_obj_or_id, pygsheets.Spreadsheet):
        spreadsheet = spreadsheet_obj_or_id
    else:
        spreadsheet = get_spreadsheet(spreadsheet_obj_or_id)
    print(FormatText.status(f'Worksheet/Tab Name: {FormatText.bold(sheet_name)}'))
    try:
        sheet = spreadsheet.worksheet_by_title(sheet_name)
        print(FormatText.status(f'Worksheet/Tab Url: {FormatText.bold(sheet.url)}')) 
        return sheet
    except Exception as error:
        msg = FormatText.error(f"Could not find sheet named '{sheet_name}'!")
        raise WorksheetNotFound(msg) from error


# get complete sheet data as pandas dataframe
def get_sheet_data(spreadsheet_obj_or_id: pygsheets.Spreadsheet | str, 
                   sheet_name : str) -> pd.DataFrame:
    sheet = get_sheet_by_name(spreadsheet_obj_or_id, sheet_name)
    return sheet.get_as_df()


# share spreadsheet publicly
def share_with_anyone(spreadsheet: pygsheets.Spreadsheet):
    print(FormatText.wait('Sharing spreadsheet publicly...'))
    print(FormatText.status(f'Url: {FormatText.bold(spreadsheet.url)}'))
    spreadsheet.share('', role='reader', type='anyone')
    

def share_with_faculty_as_editor(spreadsheet: pygsheets.Spreadsheet, faculty_email: str):
    print(FormatText.wait(f'Sharing spreadsheet with {FormatText.bold(faculty_email)}...'))
    print(FormatText.status(f'Url: {FormatText.bold(spreadsheet.url)}'))
    if re.search(RegexPattern.EMAIL_ADDRESS, faculty_email):
        # spreadsheet.share(faculty_email, role='owner', transferOwnership=True)
        spreadsheet.share(faculty_email, role='writer', type='user')
        print(FormatText.success(f'Spreadsheet shared with email: {FormatText.bold(faculty_email)}'))
    else:
        print(FormatText.error(f'Email {FormatText.bold(faculty_email)} is not in proper format.'))


# copy from a template spreadsheet and return a spreadsheet object
def copy_spreadsheet(template_id: str, title: str, folder_id: str) -> pygsheets.Spreadsheet:
    print(FormatText.wait('Copying spreadsheet from a template...'))
    print(FormatText.status(f'Template: {FormatText.bold(get_link_from_sheet_id(template_id))}'))
    print(FormatText.status(f"Spreadsheet Title: {FormatText.bold(title)}"))
    print(FormatText.status(f"Drive Folder: {FormatText.bold(get_link_from_folder_id(folder_id))}"))
    print(FormatText.status(f'Creating the new spreadsheet...'))
    spreadsheet = get_google_client().create(title=title, template=template_id, folder=folder_id)
    # finally return newly copied spreadsheet
    print(FormatText.status(f'Done copying: {FormatText.bold(get_link_from_sheet_id(spreadsheet.id))}'))
    return spreadsheet

# update cell values from dictionary in a sheet
def update_sheet_values(cell_value_dict: dict, 
                        sheet_obj: pygsheets.Worksheet | None = None, 
                        *, 
                        sheet_id: str | None = None, 
                        sheet_name: str | None = None) -> None:
    ranges = list(cell_value_dict.keys())
    # pygsheet require the values to be a list of list, i.e., matrix
    values = [val if type(val) is list else [[val]]
              for val in cell_value_dict.values()]
    # edit sheet with set_values
    if not sheet_obj:
        sheet_obj = get_sheet_by_name(sheet_id, sheet_name)
    print(FormatText.wait(f'Editing spreadsheet cells...'))
    print(FormatText.status(f'Sheet name: {FormatText.bold(sheet_obj.title)}'))
    print(FormatText.status(f'Url: {FormatText.bold(sheet_obj.url)}'))
    if len(str(cell_value_dict)) <= 100:
        print(FormatText.status(f'Setting cell values: {FormatText.bold(cell_value_dict)}'))
    else:
        print(FormatText.status(f'Setting range values: {FormatText.bold(cell_value_dict.keys())}'))
    sheet_obj.update_values_batch(ranges, values)



# directly update cells, no need to check
def update_cells_from_fields(spreadsheet: pygsheets.Spreadsheet, 
                             sheet_cell_fields_dict: dict) -> None:
    for sheet_name, cell_field_dict in sheet_cell_fields_dict.items():
        sheet = spreadsheet.worksheet_by_title(sheet_name)
        # map info field to their actual values for updating sheets
        cell_value_dict = {}
        for cell,field in cell_field_dict.items():
            value = state.info[field]
            if isinstance(value, list):
                value = ','.join(str(item) for item in value)
            cell_value_dict[cell] = value
        update_sheet_values(cell_value_dict, sheet)    

    
# allow access shenanigans
def allow_access(dest_sheet_id: str, src_sheet_id: str) -> None:
    print(FormatText.wait("Allowing sheet access..."))
    print(FormatText.status(f"Pull from: {FormatText.bold(get_link_from_sheet_id(src_sheet_id))}"))
    print(FormatText.status(f"Push to: {FormatText.bold(get_link_from_sheet_id(dest_sheet_id))}"))
    token = get_google_client().oauth.token
    url = get_allow_access_link_from_sheet_id(dest_sheet_id, src_sheet_id)
    requests.post(url, headers={'Authorization': f"Bearer {token}"})