import logging as log

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from AI.agents.content_generator_agent import ContentGeneratorAgent
from AI.agents.binary_judge_agent import BinaryJudgeAgent
from AI.agents.utilities import send_ai_thoughts
from AI.models import embedding_model
from router.route_utilities import remove_non_alphanumeric
from router.schemas.chat import Chat_Agent_Query
from AI.query_engines.record_query_engine import record_query_tool

content_generator_agent = ContentGeneratorAgent()
binary_judge_agent = BinaryJudgeAgent()

router = APIRouter()

@router.get("/get_current_embedding_model")
async def get_embedding_model(request: Request):
    try:
        return JSONResponse(content={"message": "route for getting current active embedding model in agents", "embedding_model": embedding_model.value}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error("error on getting embedding model route")
        log.error(e)
        raise e


@router.post("/chat")
async def chat_route(request: Request, data: Chat_Agent_Query):
    try:
        await send_ai_thoughts("Processing Query.", data.identifier)

        texts = []
        records_ids = []
        records_titles = []
        if data.use_records or data.number_of_chunks < 1:
            table_name = remove_non_alphanumeric(data.identifier)

            await send_ai_thoughts("Getting Records.", data.identifier)
            if data.number_of_chunks is None:
                number_of_chunks_to_retrive = 2
            else:
                number_of_chunks_to_retrive = data.number_of_chunks if data.number_of_chunks <= 10 else 10

            response = record_query_tool.get_records(table_name=table_name, question=data.query, number_of_chunks_to_retrive=number_of_chunks_to_retrive)

            await send_ai_thoughts("Checking Relevance of the Records.", data.identifier)
            
            if len(response) > 0:
                # Sort the list by the 'score' property in descending order and get the top 2
                sorted_records = sorted(response, key=lambda x: x.score, reverse=True)

                # this logic below is for getting top 2 records from sorted records
                try:
                    for i in range(len(sorted_records)):
                        texts.append(sorted_records[i].text)
                        if sorted_records[i].metadata["record_id"] not in records_ids:
                            records_ids.append(sorted_records[i].metadata["record_id"])
                            records_titles.append(sorted_records[i].metadata["title"])
                except:
                    pass
        else:
            await send_ai_thoughts("Skipping records steps.", data.identifier)


        await send_ai_thoughts("Creating Prompt.", data.identifier)

        prompt = ""
        if len(data.context) > 0:
            prompt += "The context of conversation is: "

            for message in data.context:
                prompt += f"\n{message['type']} message: {message['message']}\n"

        prompt += f"""
            question: {data.query}

            {"generate answer for the question" if len(texts) > 0 else "Answer the question mentioned above."}

            {"only use text below if the question needs, otherwise ignore text below."}

            {"text: "if len(texts) > 0 else ""}
        """
        if (len(texts) > 0):
            for text in texts:
                prompt += text + "\n"

        await send_ai_thoughts("Generating Answer.", data.identifier)
        content_agent_response = str(await content_generator_agent.run(prompt, data.identifier))
        content_agent_response = content_agent_response.split("</think>")[-1]

        return JSONResponse(content={"message": content_agent_response, "records_ids": records_ids, "records_titles": records_titles}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error("Error on chat_route")
        log.error(e)
        raise e