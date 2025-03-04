import os
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, directory: str = "temp_store") -> str:
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Define the file path
    file_path = os.path.join(directory, upload_file.filename)
    
    # Save the uploaded file
    with open(file_path, "wb") as file:
        file.write(upload_file.file.read())
    
    return file_path

def delete_file(file_path: str) -> bool:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")