from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Ruta al archivo JSON de credenciales
DIRECTORIO_CREDENCIALES = 'credentials_module.json'

# Función para iniciar sesión
def login():
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
    credenciales = GoogleDrive(gauth)
    return credenciales

# Función para crear un archivo de texto simple
def crear_archivo_texto(nombre_archivo, contenido, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'title': nombre_archivo, 'parents': [{"kind": "drive#fileLink", "id": id_folder}]})
    archivo.SetContentString(contenido)
    archivo.Upload()

# Función para subir un archivo a Google Drive
def subir_archivo(ruta_archivo, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink", "id": id_folder}]})
    archivo['title'] = ruta_archivo.split("/")[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()

# Función para descargar un archivo de Drive por ID
def bajar_archivo_por_id(id_drive, ruta_descarga):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_drive}) 
    nombre_archivo = archivo['title']
    archivo.GetContentFile(ruta_descarga + nombre_archivo)

# Función para buscar archivos en Drive
def buscar(query):
    resultado = []
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
        # Información del archivo
        print('ID Drive:', f['id'])
        print('Link de visualizacion embebido:', f['embedLink'])
        print('Link de descarga:', f['downloadUrl'])
        print('Nombre del archivo:', f['title'])
        print('Tipo de archivo:', f['mimeType'])
        print('Esta en el basurero:', f['labels']['trashed'])
        print('Fecha de creacion:', f['createdDate'])
        print('Fecha de ultima modificacion:', f['modifiedDate'])
        print('Version:', f['version'])
        print('Tamanio:', f['fileSize'])
        resultado.append(f)
    return resultado



# Código de ejecución
if __name__ == "__main__":
    # Ejemplos de uso
    ruta_archivo = '/home/falv/Escritorio/fondo.jpg'
    id_folder = '0AI_9cD6f9EEZUk9PVA'
    id_drive = '1LVdc-DUwr30kfrA30cVO3K92RVh56pmw'
    ruta_descarga = '/home/falv/Descargas/'
    
    # Ejemplo de llamada a la función para subir un archivo
    # subir_archivo(ruta_archivo, id_folder)


    crear_archivo_texto("tes", "esto es una puerba", "1FdyTzg04CGQCdPBJ5IeDjTDBH-o8oaRn" )

