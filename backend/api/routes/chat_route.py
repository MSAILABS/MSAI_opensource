import json
import logging as log

from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.agents_api.chat_api import chat_with_agents
from api.agents_api.schemas.chat_schema import Chat_Agent_Query
from core.configurations import user_identifier
from db.repository.records import get_records_count_from_db
from db.session import get_db

router = APIRouter()

@router.post("/chat")
async def chat_route(request: Request, data: Chat_Agent_Query, db: Session = Depends(get_db)):
    try:
        data.identifier = user_identifier
        records_count = get_records_count_from_db(db)

        if records_count < 1:
            data.use_records = False

        response = await chat_with_agents(data)

        data = json.loads(response.text)

        message = data["message"]
        records_ids = data["records_ids"]
        records_titles = data["records_titles"]

        return JSONResponse(content={"message": message, "records_ids": records_ids, "records_titles": records_titles}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error("Error on chat_route")
        log.error(e)
        raise e