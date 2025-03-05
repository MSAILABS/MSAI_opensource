import os
import logging as log
from turtle import title
from fastapi import HTTPException, UploadFile
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.repository.records import add_record_into_db, delete_record_from_db, get_all_records_from_db, update_record_in_db
from db.session import get_db

from utilities.files import delete_file, save_upload_file
from utilities.text_extract import extract_text

router = APIRouter()
        
@router.get("/get_records")
async def get_records(db: Session = Depends(get_db)):
    try:
        records = get_all_records_from_db(db)
        return JSONResponse(content={"records": records}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error("error on get_records route")
        log.error(e)
        return JSONResponse(content={"error": "Error on getting all records"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/add_record")
async def add_record(file: UploadFile, db: Session = Depends(get_db)):
    file_path = ""
    try:
        # Check file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".docx", ".doc", ".txt", ".pdf"]:
            raise HTTPException(status_code=400, detail="Invalid file format. Only .docx, .doc, .txt, .pdf are allowed.")
        
        file_path = save_upload_file(file)
        
        # Extract data from file and save to db
        data = extract_text(file_path)

        # Get file name as title
        title = os.path.splitext(file.filename)[0]

        # Assuming you have a function save_to_db to save data to the database
        record = add_record_into_db(title, data, db)

        if record is not None:
            return JSONResponse(content={"message": "Record added successfully"}, status_code=status.HTTP_201_CREATED)
        
        return JSONResponse(content={"error": "Error on adding record"}, status_code=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        log.error("error on add_record route")
        log.error(e)
        raise e
    finally:
        delete_file(file_path)
    
@router.get("/delete_record/{record_id}")
async def delete_record(request: Request, record_id: int, db: Session = Depends(get_db)):
    try:
        # Assuming you have a function save_to_db to save data to the database
        is_record_deleted = delete_record_from_db(record_id, db)

        if is_record_deleted:
            return JSONResponse(content={"message": "Record deleted successfully"}, status_code=status.HTTP_200_OK)
        
        return JSONResponse(content={"error": "Error on deleting record"}, status_code=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        log.error("error on delete_record route")
        log.error(e)
        raise e


class Edit_Record(BaseModel):
    title: str
    description: str

@router.post("/edit_record/{record_id}")
async def edit_record(request: Request, record_id: int, data: Edit_Record, db: Session = Depends(get_db)):
    try:
        is_record_updated = update_record_in_db(record_id=record_id, title=data.title, description=data.description, db=db)

        if is_record_updated:
            return JSONResponse(content={"message": "Record updated"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Record could not updated"}, status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        log.error("Error on editing the record")
        log.error(e)
        raise e
