from llama_index.core.agent import ReActAgent

from AI.agents.base_class.base_agent import Base_Agent
from AI.agents.utilities import run_agent_task
from AI.models import Models

class BinaryJudgeAgent(Base_Agent):
    def __init__(self):
        self.name = "Binary_judge_agent"
        self.description = 'Agent used to check prompt and only give answer as "yes" or "no".'
        self.purpose = 'you are an ai agent used to check prompt and only give answer as "yes" or "no". If you need more information, ask for it.'
        self.agent = None
        self.llm = Models.get_LLM(Models.AIModels.OLLAMA)
        self.__setup_agent__()

    def __setup_agent__(self):
        if self.agent == None:
            tools = []

            self.agent = ReActAgent.from_tools(tools, llm=self.llm, verbose=True, max_iterations=10)

    async def run(self, text:str = "", email:str = "", *args, **kwargs):
        parameters = ""

        if (args):
            for arg in args:
                parameters += str(arg)

        if (kwargs):
            for key in kwargs:
                parameters += f"{kwargs}: "
                parameters += f"{kwargs[key]}\n"

        prompt = f"""
        your purpose is {self.purpose}

        {parameters}

        Instructions:
        1. DO NOT use any tools, just give answer as "yes" or "no".
        2. Your reply should Only have "yes" or "no". DO NOT ADD any other text.

        text by super ai agent:
        {"" if text is None else text}
        """

        response = await run_agent_task(self.agent, prompt, email)

        # response = self.agent.chat(prompt)

        return response