from datetime import datetime
import logging as log

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from llama_index.core.schema import Document
from sqlalchemy import table

from AI.agents.content_generator_agent import ContentGeneratorAgent
from AI.agents.binary_judge_agent import BinaryJudgeAgent
from db.repository.records import add_data_into_vector_store, delete_records_group, delete_user_record
from router.route_utilities import remove_non_alphanumeric
from router.schemas.records import RecordClusterDeletion, RecordData, RecordDataDelete, RecordDataQuery
from AI.models import embedding_model

router = APIRouter()

content_generator_agent = ContentGeneratorAgent()
binary_judge_agent = BinaryJudgeAgent()

@router.post("/add_record_into_vector_db")
async def add_record_into_vector_db(request: Request, record_data: RecordData):
    try:
        table_name = f"{remove_non_alphanumeric(record_data.identifier)}{remove_non_alphanumeric(record_data.cluster_name)}" 

        # deleting old record if record is already present
        # reason for this that if user vectorized record previously using different embedding_model and then after change model.
        # it is possible that record is updated and we have to redo vectorization because previous vectorization does not match old text.
        delete_user_record(table_name=table_name, record_id=record_data.record_id)

        isSaved = False
        texts = record_data.record_description.split("===msai-labs page break===")

        full_text = ""

        for index, text in enumerate(texts):
            full_text += text

            if (full_text == ""):
                continue
            
            if len(full_text) < 2000 and index < len(texts) - 1:
                continue
            
            response = ""

            if len(full_text) < 2000:
                prompt = f"""
                    Give a summary of this text below.

                    {full_text}
                """

                response = str(await content_generator_agent.run(text=prompt))

                response = response.split("</think>")[-1]
            else:
                response = full_text

            now = datetime.now()
            new_metadata = {
                "record_id": record_data.record_id,
                "upload_year": now.year,
                "upload_month": now.month,
                "upload_day": now.day,
                "title": record_data.record_title,
                "summary": full_text
            }

            doc = Document(text=full_text, metadata=new_metadata)
            
            isSaved = add_data_into_vector_store(table_name=table_name, doc=doc)

            full_text = ""

        if (isSaved):
            return JSONResponse(content={"message": "Record data added into vector store", "embedding_model": embedding_model.value}, status_code=status.HTTP_201_CREATED)
        else:
            return JSONResponse(content="Cannot add record data into vector store", status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        log.error("error on saving record into vector db")
        log.error(e)
        raise e


@router.post("/delete_record_data_from_vector_db")
async def remove_record_from_vector_db(request: Request, data: RecordDataDelete):
    try:
        table_name = f"{remove_non_alphanumeric(data.identifier)}{remove_non_alphanumeric(data.cluster_name)}" 

        is_deleted = delete_user_record(table_name=table_name, record_id=data.record_id)

        if (is_deleted):
            return JSONResponse(content="Record data deleted", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content="Cannot delete record data", status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        log.error("error on removing record data")  
        log.error(e)
        raise e



@router.post("/update_record_data_in_vector_db")
async def update_record_in_vector_db(request: Request, data: RecordData):
    try:
        delete_record = RecordDataDelete(record_id=data.record_id, identifier=data.identifier, cluster_name=data.cluster_name)
        res = await remove_record_from_vector_db(request, delete_record)

        if res.status_code == 200:
            res = await add_record_into_vector_db(request, data)

            if res.status_code == 201:
                    return JSONResponse(content="Record data updated successfully", status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content="Cannot update record data", status_code=status.HTTP_400_BAD_REQUEST)
        else:
            return JSONResponse(content="Cannot update record data", status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        log.error("error on updating record data")
        log.error(e)
        raise e
    

@router.post("/delete_records_cluster")
async def delete_records_cluster(request: Request, data: RecordClusterDeletion):
    try:
        table_name = f"{remove_non_alphanumeric(data.identifier)}{remove_non_alphanumeric(data.cluster_name)}" 
        is_group_delete = delete_records_group(table_name = table_name)

        if is_group_delete:
            return JSONResponse(content="Records Cluster deleted successfully", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content="Cannot delete records cluster", status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        log.error("error on delete_records_cluster route")
        log.error(e)
        raise e
    


@router.post("/record_query_route")
async def record_query_route(request: Request, data: RecordDataQuery):
    try:
        pass
    except Exception as e:
        log.error("error on query record data")
        log.error(e)
        raise e



