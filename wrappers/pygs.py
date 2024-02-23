import requests
import pygsheets as pygs
from bot_variables.config import FileName

# authorization
def get_google_client():
    return pygs.authorize(client_secret = FileName.GOOGLE_CREDENTIALS)


# get a specific sheet by name from a spreadsheet
def get_sheet(spreadsheet_id, sheet_name):
    spreadsheet = get_google_client().open_by_key(spreadsheet_id)
    return spreadsheet.worksheet_by_title(sheet_name)


# get complete sheet data as pandas dataframe
def get_sheet_data(spreadsheet_id, sheet_name):
    sheet = get_sheet(spreadsheet_id, sheet_name)
    return sheet.get_as_df()

