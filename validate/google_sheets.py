from pygsheets import AuthenticationError
from wrappers.pygs import get_google_client
from wrappers.utils import format_error_msg, format_success_msg

# TODO: check for sheets.googleapis.com-python.json
#       if that json file exists, success
#       else prompt for browser login

def check_google_credentials():
    try:
        get_google_client()
        print(format_success_msg("Google authorization was successful."))
    except Exception as error:
        msg = format_error_msg("Google authorization failed!"
                               " Did you forget to provide the credentials.json file?")
        raise AuthenticationError(msg) from error