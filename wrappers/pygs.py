import requests
import pygsheets as pygs
from singletons.bot_config import FileName


def get_google_client():
    return pygs.authorize(client_secret = FileName.GOOGLE_CREDENTIALS)