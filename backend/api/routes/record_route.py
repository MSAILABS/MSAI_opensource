from datetime import datetime
import os, json
import logging as log
from fastapi import HTTPException, UploadFile
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from httpx import Response
from sqlalchemy.orm import Session

from api.agents_api.chat_api import get_agents_embedding_model
from api.agents_api.records_api import add_record_into_vector_db, remove_record_from_vector_db, update_record_in_vector_db
from api.agents_api.schemas.records_schema import Edit_Record, RecordData, RecordDataDelete
from db.models.records import Records
from db.repository.records import add_record_into_db, delete_record_from_db, get_all_records_from_db, get_record_by_id, mark_record_as_vectorized, update_record_in_db
from db.session import get_db

from utilities.files import delete_file, save_upload_file
from utilities.text_extract import extract_text

from core.configurations import user_identifier

router = APIRouter()
        
@router.get("/get_records/{cluster_id}")
async def get_records(cluster_id: int, db: Session = Depends(get_db)):
    try:
        res = await get_agents_embedding_model()

        embedding_model = json.loads(res.text)["embedding_model"]

        records = get_all_records_from_db(cluster_id, db)
        return JSONResponse(content={"records": records, "embedding_model": embedding_model}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error("error on get_records route")
        log.error(e)
        return JSONResponse(content={"error": "Error on getting all records"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/add_record/{cluster_id}")
async def add_record(file: UploadFile, cluster_id: int, db: Session = Depends(get_db)):
    file_path = ""
    try:
        # Check file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".docx", ".txt", ".pdf"]:
            raise HTTPException(status_code=400, detail="Invalid file format. Only .docx, .doc, .txt, .pdf are allowed.")
        
        file_path = save_upload_file(file)
        
        # Extract data from file and save to db
        data = extract_text(file_path)

        # Get file name as title
        title = os.path.splitext(file.filename)[0]

        # Assuming you have a function save_to_db to save data to the database
        record = add_record_into_db(title=title, text=data, cluster_id=cluster_id, db=db)

        if record is None:
            return JSONResponse(content={"error": "Error on adding record"}, status_code=status.HTTP_400_BAD_REQUEST)

        return JSONResponse(content={"message": "Record added successfully"}, status_code=status.HTTP_201_CREATED)


        # if record is not None:
        #     record_data = RecordData(
        #         record_id=record.id, 
        #         record_description=record.description, 
        #         record_title=record.title, 
        #         record_upload_date=str(record.upload_date),
        #         identifier=user_identifier
        #     )
        
            # res: Response = await add_record_into_vector_db(record_data)

            # if res.status_code == 201:
                # return JSONResponse(content={"message": "Record added successfully"}, status_code=status.HTTP_201_CREATED)
            # else:
            #     return JSONResponse(content={"message": "Record added successfully on backend, but not on agents db"}, status_code=status.HTTP_201_CREATED) 
    except Exception as e:
        log.error("error on add_record route")
        log.error(e)
        raise e
    finally:
        delete_file(file_path)


@router.get("/add_record_into_vector_db/{record_id}")
async def vectorize_record_route(request: Request, record_id: int, db: Session = Depends(get_db)):
    try:
        record, cluster = get_record_by_id(record_id, db)

        if record is None:
            return JSONResponse(content={"message": "Incorrect record id, can't find record"}, status_code=status.HTTP_400_BAD_REQUEST)
        
        record_data = RecordData(
            record_id=record.id, 
            record_description=record.description, 
            record_title=record.title, 
            record_upload_date=str(record.upload_date),
            identifier=user_identifier,
            cluster_name=cluster.title
        )

        res: Response = await add_record_into_vector_db(record_data)

        if res.status_code == 201:
            embedding_model = json.loads(res.text)["embedding_model"]
            record = mark_record_as_vectorized(record.id, embedding_model, db)

            if record is None:
                return JSONResponse(content={"message": "Record vectorized, But not marked as vectorized"}, status_code=status.HTTP_201_CREATED)
            else:
                return JSONResponse(content={"message": "Record vectorized successfully"}, status_code=status.HTTP_201_CREATED)
        else:
            return JSONResponse(content={"message": "Record vectorize failure."}, status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        log.error("error on add_record_into_vector_db route")
        log.error(e)
        raise e

@router.get("/delete_record/{record_id}")
async def delete_record(request: Request, record_id: int, db: Session = Depends(get_db)):
    try:
        # Assuming you have a function save_to_db to save data to the database
        is_record_deleted, cluster = delete_record_from_db(record_id, db)

        if is_record_deleted:
            record_data_delete = RecordDataDelete(
                record_id=record_id,
                identifier=user_identifier,
                cluster_name=cluster.title
            )
            
            res: Response = await remove_record_from_vector_db(record_data_delete)

            if res.status_code == 200:
                return JSONResponse(content={"message": "Record deleted successfully"}, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content={"message": "Record deleted successfully, but not on agents db"}, status_code=status.HTTP_200_OK)
        
        return JSONResponse(content={"error": "Error on deleting record"}, status_code=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        log.error("error on delete_record route")
        log.error(e)
        raise e




@router.post("/edit_record/{record_id}")
async def edit_record(request: Request, record_id: int, data: Edit_Record, db: Session = Depends(get_db)):
    try:
        is_record_updated, cluster = update_record_in_db(record_id=record_id, title=data.title, description=data.description, db=db)

        if is_record_updated:
            record_data = RecordData(
                record_id=record_id, 
                record_description=data.description, 
                record_title=data.title, 
                record_upload_date=str(datetime.now()),
                identifier=user_identifier,
                cluster_name=cluster.title
            )
            res: Response =  await update_record_in_vector_db(record_data)

            if res.status_code == 200:
                return JSONResponse(content={"message": "Record updated"}, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content={"message": "Record updated, but not on agents db"}, status_code=status.HTTP_200_OK)


        else:
            return JSONResponse(content={"message": "Record could not updated"}, status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        log.error("Error on editing the record")
        log.error(e)
        raise e
