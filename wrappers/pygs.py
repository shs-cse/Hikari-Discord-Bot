import requests
import pygsheets as pygs
from bot_variables.config import FileName


def get_google_client():
    return pygs.authorize(client_secret = FileName.GOOGLE_CREDENTIALS)