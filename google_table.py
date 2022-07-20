import time

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials	
from data.config import *


credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                   'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4',
                                    http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

driveService = apiclient.discovery.build('drive', 'v3',
                                         http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API


def append_to_sheet(data, cell, list_name='Лист номер один'):
    results = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range=f"{list_name}!{cell}",
        valueInputOption="RAW",
        body={
            'values': [[data]]
        }).execute()


if __name__=='__main__':
    append_to_sheet(data='2', cell='A1')
    print(time.time())
    append_to_sheet(data='2', cell='A2')
    print(time.time())
    append_to_sheet(data='2', cell='A3')
    print(time.time())
    append_to_sheet(data='2', cell='A4')
    print(time.time())