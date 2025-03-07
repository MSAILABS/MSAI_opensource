import json
from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse
from aio_pika import connect_robust, ExchangeType

from core.configurations import RABBITMQ_SETTINGS, user_identifier

router = APIRouter()

async def consume_message(identifier):
    EXCHANGE_NAME = "msai"
    connection = await connect_robust(RABBITMQ_SETTINGS)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.DIRECT, durable=True)
    queue_name = f'{identifier}'
    await channel.queue_delete(queue_name=queue_name)
    queue = await channel.declare_queue(queue_name)
    await queue.bind(exchange, routing_key=identifier)

    async for message in queue:
        async with message.process():
            data = json.dumps(json.loads(message.body.decode()))
            print('Consuming Messaging...')
            print(data)
            yield data
            print('Message Consumed')


async def listen_rmq(identifier: str):
    async for message in consume_message(identifier):
        yield message


@router.get("/sse")
async def sse_endpoint(request: Request):
    print(f'Connecting AI_AGENT SSE for user => {user_identifier}')

    return EventSourceResponse(listen_rmq(user_identifier))


