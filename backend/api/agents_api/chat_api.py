import httpx
from api.agents_api.schemas.chat_schema import Chat_Agent_Query
from core.configurations import BASE_URL

async def chat_with_agents(data: Chat_Agent_Query):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(f"{BASE_URL}/chat", json=data.model_dump())
        return response