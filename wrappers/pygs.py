import requests
import pygsheets as pygs
from consts import FileName
from wrappers.utils import format_error_msg, format_success_msg, format_warning_msg


def check_google_creds():
    try:
        get_google_client()
        print(format_success_msg("Google authorization was successful."))
    except Exception as error:
        msg = format_error_msg("Google authorization failed!"
                               " Did you forget to provide the credentials.json file?")
        raise pygs.AuthenticationError(msg) from error
    

def get_google_client():
    return pygs.authorize(client_secret = FileName.GOOGLE_CREDENTIALS)