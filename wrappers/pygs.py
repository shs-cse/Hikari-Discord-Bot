import requests
import pygsheets as pygs
from bot_variables.config import FileName

# authorization
def get_google_client():
    return pygs.authorize(client_secret = FileName.GOOGLE_CREDENTIALS)


# get a spreadsheet object
def get_spreadsheet(spreadsheet_id):
    return get_google_client().open_by_key(spreadsheet_id)


# get a specific sheet (tab) by name from a spreadsheet
def get_sheet_by_name(spreadsheet_id, sheet_name):
    return get_spreadsheet(spreadsheet_id).worksheet_by_title(sheet_name)


# get complete sheet data as pandas dataframe
def get_sheet_data(spreadsheet_id, sheet_name):
    sheet = get_sheet_by_name(spreadsheet_id, sheet_name)
    return sheet.get_as_df()



def copy_spreadsheet(template_id, title, folder_id, set_sheet_cells=None):
    google_client = get_google_client()
    template = google_client.open_by_key(template_id)
    spreadsheet = google_client.create(title=title, template=template, folder=folder_id)
    # populate values if provided
    if set_sheet_cells:
        for sheet_name, set_values_dict in set_sheet_cells.items():
            sheet = spreadsheet.worksheet_by_title(sheet_name)
            update_sheet_values(set_values_dict, sheet)
    # finally return newly copied sheet's id
    return spreadsheet.id


# update cell values from dictionary in a sheet
def update_sheet_values(set_values_dict, sheet_obj=None, sheet_id=None, sheet_name=None):
    ranges = list(set_values_dict.keys())
    # pygsheet require the values to be a list of list, i.e., matrix
    values = [val if type(val) is list else [[val]]
              for val in set_values_dict.values()]
    # edit sheet with set_values
    if not sheet_obj:
        sheet_obj = get_sheet_by_name(sheet_id, sheet_name)
    sheet_obj.update_values_batch(ranges, values)