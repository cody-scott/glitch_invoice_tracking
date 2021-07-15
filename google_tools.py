from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

scopes = ['https://www.googleapis.com/auth/spreadsheets']
service_account_file = 'api_credentials.json'

def load_g_data():
    # cheat it since i have a local file of creds
    if os.getenv("LOCAL") is not None:
        return

    g_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    g_data = os.getenv('GOOGLE_CREDENTIALS')
    
    with open(g_path, 'w') as fl:
        fl.write(g_data)



def get_service():
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)
    service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
    return service
