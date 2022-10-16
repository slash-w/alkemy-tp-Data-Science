from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account

import pandas as pd
import datetime, os

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Genera el nombre entero del path del CSV y crea las carpetas
def new_namer(name, make_dir = False):
    meses = ['enero',      'febrero', 'marzo',     'abril',
           'mayo',       'junio',   'julio',     'agosto',
           'septiembre', 'octubre', 'noviembre', 'diciembre']
    time = datetime.datetime.now()
  
    if make_dir:
        # --- Path ---
        new_dir = f'./{name}/{time.year}-{meses[time.month - 1]}/'
        try: #FileExistsError: [WinError 183]
            os.makedirs(new_dir)
        except:
            pass
    else:
        new_dir = f'./{name}/{time.year}-{meses[time.month - 1]}/'
    # --- Nombre CSV ---
    file_name = f'{name}-{time.day}-{time.month}-{time.year}'

    return new_dir+file_name+'.csv'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Toma el url del google sheet y devuelve su ID
def get_sheet_id(url):
  a = url.split('/')
  return a[5]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Usando la API de Google y Pandas crea los archivos CSV
def sheet_to_csv(name, custom_range, url):
  
    sheet_id = get_sheet_id(url)
    # Pide el token de autorizacion y settea la API para read only
    service_acc_file = 'token.json'
    sheet_scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = service_account.Credentials.from_service_account_file(
            service_acc_file, scopes=sheet_scopes)

    service = build('sheets', 'v4', credentials=creds)
    # LLama la API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=custom_range).execute() # 'Datos Argentina - Salas de Cine!A1:X'
  
    values = result.get('values', [])

    df = pd.DataFrame(values)
    df.to_csv(new_namer(name, True))
