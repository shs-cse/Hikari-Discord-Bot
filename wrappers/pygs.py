import requests
import pygsheets as pygs
from wrappers.utils import FormatText, get_link_from_sheet_id, get_link_from_folder_id
from bot_variables.config import FileName
from bot_variables import state

# TODO: change all sheet to either spreadsheet or worksheet to clear confusions
# TODO: check if file in trash

# authorization
def get_google_client():
    return pygs.authorize(client_secret = FileName.GOOGLE_CREDENTIALS)


# get a spreadsheet object
def get_spreadsheet(spreadsheet_id):
    print(FormatText.wait("Fetching spreadsheet..."))
    msg = f"Url: {FormatText.BOLD}{get_link_from_sheet_id(spreadsheet_id)}"
    print(FormatText.status(msg))
    return get_google_client().open_by_key(spreadsheet_id)


# get a specific sheet (tab) by name from a spreadsheet
def get_sheet_by_name(spreadsheet_id, sheet_name):
    spreadsheet = get_spreadsheet(spreadsheet_id)
    print(FormatText.status(f'Sheet/Tab Name: {sheet_name}'))
    return spreadsheet.worksheet_by_title(sheet_name)


# get complete sheet data as pandas dataframe
def get_sheet_data(spreadsheet_id, sheet_name):
    sheet = get_sheet_by_name(spreadsheet_id, sheet_name)
    return sheet.get_as_df()


# share spreadsheet publicly
def share_with_anyone(spreadsheet: pygs.Spreadsheet):
    print(FormatText.wait('Sharing spreadsheet publicly...'))
    print(FormatText.status(f'Url: {FormatText.BOLD}{spreadsheet.url}'))
    spreadsheet.share('', role='reader', type='anyone')


# copy from a template spreadsheet and return a spreadsheet object
def copy_spreadsheet(template_id, title, folder_id):
    print(FormatText.wait('Copying spreadsheet from a template...'))
    print(FormatText.status(f'Template: {FormatText.BOLD}{get_link_from_sheet_id(template_id)}'))
    print(FormatText.status(f"Spreadsheet Title: {FormatText.BOLD}{title}"))
    print(FormatText.status(f"Drive Folder: {FormatText.BOLD}{get_link_from_folder_id(folder_id)}"))
    print(FormatText.status(f'Creating the new spreadsheet...'))
    spreadsheet = get_google_client().create(title=title, template=template_id, folder=folder_id)
    # finally return newly copied spreadsheet
    print(FormatText.status(f'Done copying: {FormatText.BOLD}{get_link_from_sheet_id(spreadsheet.id)}'))
    return spreadsheet


# update cell values from dictionary in a sheet
def update_sheet_values(cell_value_dict, sheet_obj=None, *, sheet_id=None, sheet_name=None):
    ranges = list(cell_value_dict.keys())
    # pygsheet require the values to be a list of list, i.e., matrix
    values = [val if type(val) is list else [[val]]
              for val in cell_value_dict.values()]
    # edit sheet with set_values
    if not sheet_obj:
        sheet_obj = get_sheet_by_name(sheet_id, sheet_name)
    print(FormatText.wait(f'Editing spreadsheet cells...'))
    print(FormatText.status(f'Sheet name: {FormatText.BOLD}{sheet_obj.title}'))
    print(FormatText.status(f'Url: {FormatText.BOLD}{sheet_obj.url}'))
    print(FormatText.status(f'Setting cell values: {FormatText.BOLD}{cell_value_dict}'))
    sheet_obj.update_values_batch(ranges, values)



# directly update cells, no need to check
def update_cells_from_fields(spreadsheet: pygs.Spreadsheet, sheet_cell_fields_dict: dict):
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
def allow_access(dest_sheet_id, src_sheet_id):
    print(FormatText.wait("Allowing sheet access..."))
    print(FormatText.status(f"Pull from: {FormatText.BOLD}{get_link_from_sheet_id(src_sheet_id)}"))
    print(FormatText.status(f"Push to: {FormatText.BOLD}{get_link_from_sheet_id(dest_sheet_id)}"))
    token = get_google_client().oauth.token
    url = f"https://docs.google.com/spreadsheets/d/{dest_sheet_id}"
    url += f"/externaldata/addimportrangepermissions?donorDocId={src_sheet_id}"
    requests.post(url, headers={'Authorization': f"Bearer {token}"})