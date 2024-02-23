from os import path
from bot_variables.config import FileName
from pygsheets import AuthenticationError
from wrappers.pygs import get_google_client
from wrappers.utils import FormatText

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
    

def check_enrolment():
    ...