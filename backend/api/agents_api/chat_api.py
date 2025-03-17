import httpx
from api.agents_api.schemas.chat_schema import Chat_Agent_Query
from core.configurations import BASE_URL

async def chat_with_agents(data: Chat_Agent_Query):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(f"{BASE_URL}/chat", json=data.model_dump())
        return response
    

async def get_agents_embedding_model():
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.get(f"{BASE_URL}/get_current_embedding_model")
        return response