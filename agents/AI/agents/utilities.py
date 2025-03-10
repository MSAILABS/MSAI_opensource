import json
import logging as log

from aio_pika import connect_robust, Message, ExchangeType
from llama_index.core.agent import ReActAgent
from llama_index.core.base.agent.types import Task

async def send_ai_thoughts(thought, identifier, retry = False):
    try:
        RABBITMQ_SETTINGS = "amqp://guest:guest@rabbitmq/"
        EXCHANGE_NAME = "ai_thoughts"

        connection = await connect_robust(RABBITMQ_SETTINGS)
        channel = await connection.channel()
        exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.DIRECT, durable=True)

        # Declare Queue and Bind to Exchange
        queue = await channel.declare_queue(identifier)
        await queue.bind(exchange, routing_key=identifier)

        # Publish Message
        message = Message(
            body=json.dumps(thought).encode(),
            delivery_mode=2  # Persistent message
        )
        await exchange.publish(message, routing_key=identifier)

        log.info(f"identifier: {identifier}, response_text: {thought}")

        await connection.close()
    except Exception as e:
        log.error("error on sending the thought")
        log.error(e)

# function for sending message to query from anywhere
async def send_to_backend(reasoning, identifier):
    if (identifier != ""):
        await send_ai_thoughts(reasoning, identifier)

async def run_agent_task(agent: ReActAgent, prompt, identifier = ""):
    # create task
    task: Task = agent.create_task(prompt)

    step_output = agent.run_step(task.task_id)

    try:
        reasoning = task.extra_state['current_reasoning'][-1].thought
    except:
        reasoning = task.extra_state['current_reasoning'][-1].observation

    await send_to_backend(reasoning, identifier)

    while not step_output.is_last:
        step_output = agent.run_step(task.task_id)
        await send_to_backend(reasoning, identifier)

    response = agent.finalize_response(task.task_id)

    return response