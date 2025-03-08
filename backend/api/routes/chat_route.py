import json
import logging as log

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from api.agents_api.chat_api import chat_with_agents
from api.agents_api.schemas.chat_schema import Chat_Agent_Query
from core.configurations import user_identifier

router = APIRouter()

@router.post("/chat")
async def chat_route(request: Request, data: Chat_Agent_Query):
    try:
        data.identifier = user_identifier
        response = await chat_with_agents(data)

        data = json.loads(response.text)
        print(response.text)

        return JSONResponse(content={"message": data["message"]}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error("Error on chat_route")
        log.error(e)
        raise e