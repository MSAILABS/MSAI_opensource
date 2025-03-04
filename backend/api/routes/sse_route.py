import json
from fastapi import APIRouter, Request
from aio_pika import connect_robust, ExchangeType

from core.configurations import RABBITMQ_SETTINGS

router = APIRouter()

async def consume_message(username):
    EXCHANGE_NAME = "msai"
    connection = await connect_robust(RABBITMQ_SETTINGS)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.DIRECT, durable=True)
    queue_name = f'{username}'
    await channel.queue_delete(queue_name=queue_name)
    queue = await channel.declare_queue(queue_name)
    await queue.bind(exchange, routing_key=username)

    async for message in queue:
        async with message.process():
            data = json.dumps(json.loads(message.body.decode()))
            print('Consuming Messaging...')
            print(data)
            yield data
            print('Message Consumed')


async def listen_rmq(username: str):
    async for message in consume_message(username):
        yield message


@router.get("/sse/{user_identifier}")
async def sse_endpoint(request: Request, user_identifier: str):
    print(f'Connecting AI_AGENT SSE for user => {user_identifier}')


