from AI.agents.base_class.base_agent import Base_Agent
from AI.agents.utilities import run_agent_task
from AI.models import Models

from llama_index.core.agent import ReActAgent


class ContentGeneratorAgent(Base_Agent):
    def __init__(self):
        self.name = "content_generator_agent"
        self.description = "Agent used to generate content based on user input."
        self.purpose = "You are an AI agent responsible to generate content based on user input. If you need more information, ask for it."
        self.agent = None
        self.llm = Models.get_LLM(Models.AIModels.OLLAMA)
        self.__setup_agent__()

    def __setup_agent__(self):
        if self.agent == None:
            tools = []

            self.agent = ReActAgent.from_tools(tools, llm=self.llm, verbose=True, max_iterations=10)

    async def run(self, text:str = "", identifier:str = "", *args, **kwargs):
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
        1. If tools is not provided generate content yourself.

        prompt:
        { "" if text is None else text}
        """

        # response = self.agent.chat(prompt)

        response = await run_agent_task(self.agent, prompt, identifier)

        return response