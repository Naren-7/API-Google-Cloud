import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pandas as pd

# Ruta al archivo JSON de credenciales
DIRECTORIO_CREDENCIALES = 'credentials_module.json'

# Función para iniciar sesión en Google Drive
def login_to_drive():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = DIRECTORIO_CREDENCIALES
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(DIRECTORIO_CREDENCIALES)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(DIRECTORIO_CREDENCIALES)
    drive = GoogleDrive(gauth)
    return drive

# Función para obtener el archivo .xlsx de Google Drive y convertirlo a DataFrame
def get_xlsx_as_dataframe(file_id):
    drive = login_to_drive()
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile('temp.xlsx')  # Descarga el archivo como temp.xlsx
    df = pd.read_excel('temp.xlsx')  # Lee el archivo usando pandas
    return df









