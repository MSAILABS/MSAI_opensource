import logging as log

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from AI.agents.content_generator_agent import ContentGeneratorAgent
from AI.agents.binary_judge_agent import BinaryJudgeAgent
from AI.agents.utilities import send_ai_thoughts
from router.route_utilities import remove_non_alphanumeric
from router.schemas.chat import Chat_Agent_Query
from AI.query_engines.record_query_engine import record_query_tool

content_generator_agent = ContentGeneratorAgent()
binary_judge_agent = BinaryJudgeAgent()

router = APIRouter()

@router.post("/chat")
async def chat_route(request: Request, data: Chat_Agent_Query):
    try:
        await send_ai_thoughts("Processing Query.", data.identifier)
        await send_ai_thoughts("Checking if this query needs records.", data.identifier)
        prompt = f"""
        question: {data.query}
        
        Does this question needs records for generating answer?"""

        binary_judge_agent_response = str(await binary_judge_agent.run(prompt, data.identifier))
        binary_judge_agent_response = binary_judge_agent_response.split("</think>")[-1]

        texts = []
        if (binary_judge_agent_response.lower().find("no") == -1):
            await send_ai_thoughts("Query need records information.", data.identifier)
            table_name = remove_non_alphanumeric(data.identifier)

            await send_ai_thoughts("Getting Records.", data.identifier)
            response = record_query_tool.get_records(table_name=table_name, question=data.query)


            await send_ai_thoughts("Checking Relevance of the Records.", data.identifier)
            for node in response:
                if node.score > 0.2:
                    texts.append(node.text)
        else:
            await send_ai_thoughts("Query does not need records information.", data.identifier)


        await send_ai_thoughts("Creating Prompt.", data.identifier)
        prompt = f"""
            question: {data.query}

            {"generate answer using text below for the question provided above." if len(texts) > 0 else "Answer the question mentioned above."}

            {"text: "if len(texts) > 0 else ""}
        """
        if (len(texts) > 0):
            for text in texts:
                prompt += text + "\n"

        await send_ai_thoughts("Generating Answer.", data.identifier)
        content_agent_response = str(await content_generator_agent.run(prompt, data.identifier))
        content_agent_response = content_agent_response.split("</think>")[-1]

        return JSONResponse(content={"message": content_agent_response}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error("Error on chat_route")
        log.error(e)
        raise e