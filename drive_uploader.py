from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def init_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Deschide browser pentru autentificare
    drive = GoogleDrive(gauth)
    return drive

def upload_to_drive(drive, local_path, client_name, year="2025"):
    base_folder_name = "Kuziini_Devize"
    year_folder_name = year
    client_folder_name = client_name.replace(" ", "_")

    def get_or_create_folder(name, parent_id=None):
        query = f"title='{name}' and mimeType='application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        file_list = drive.ListFile({'q': query}).GetList()
        if file_list:
            return file_list[0]['id']
        folder_metadata = {
            'title': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            folder_metadata['parents'] = [{'id': parent_id}]
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']

    base_id = get_or_create_folder(base_folder_name)
    year_id = get_or_create_folder(year_folder_name, parent_id=base_id)
    client_id = get_or_create_folder(client_folder_name, parent_id=year_id)

    filename = os.path.basename(local_path)
    gfile = drive.CreateFile({'title': filename, 'parents': [{'id': client_id}]})
    gfile.SetContentFile(local_path)
    gfile.Upload()