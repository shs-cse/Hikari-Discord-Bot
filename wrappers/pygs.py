import requests
import pygsheets as pygs
from consts import FileName, Color


def check_google_creds():
    try:
        get_google_client()
        msg = Color.OK_GREEN
        msg += "✔ Google authorization was successful."
        msg += Color.RESET
        print(msg)
    except Exception as error:
        msg = '\n'
        msg += Color.FAIL
        msg += "✘ Google authorization failed!"
        msg += " Did you forget to provide the credentials.json file?"
        msg += Color.RESET
        raise pygs.AuthenticationError(msg) from error
    

def get_google_client():
    return pygs.authorize(client_secret = FileName.GOOGLE_CREDENTIALS)