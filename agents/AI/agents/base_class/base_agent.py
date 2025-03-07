from abc import ABC, abstractmethod
from typing import List

from llama_index.core.llms import ChatMessage

class Base_Agent(ABC):
    name = ""
    description = ""
    purpose = ""
    agents = None
    agent = None
    llm = None
    chat_history: List[ChatMessage] = []

    @abstractmethod
    def __setup_agent__(self):
        pass

    @abstractmethod
    def run(self):
        pass
