import httpx
from api.agents_api.schemas.records_schema import RecordClusterDeletion, RecordData, RecordDataDelete, RecordDataQuery
from core.configurations import BASE_URL

async def add_record_into_vector_db(record_data: RecordData):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(f"{BASE_URL}/add_record_into_vector_db", json=record_data.model_dump())
        return response

async def remove_record_from_vector_db(data: RecordDataDelete):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(f"{BASE_URL}/delete_record_data_from_vector_db", json=data.model_dump())
        return response

async def update_record_in_vector_db(data: RecordData):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(f"{BASE_URL}/update_record_data_in_vector_db", json=data.model_dump())
        return response

async def record_query_route(data: RecordDataQuery):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(f"{BASE_URL}/record_query_route", json=data.model_dump())
        return response
    
async def delete_records_cluster(data: RecordClusterDeletion):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(f"{BASE_URL}/delete_records_cluster", json=data.model_dump())
        return response
