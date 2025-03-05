import logging as log

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router("/add_record_into_vector_db")
async def add_record_into_vector_db(request: Request):
    try:
        return JSONResponse(content={"message": "record added into vector db"}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        log.error("error on saving record into vector db")
        log.error(e)
        raise e

