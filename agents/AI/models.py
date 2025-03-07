from abc import abstractmethod
import os
from enum import Enum
from dotenv import load_dotenv

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


# loading environment variables
load_dotenv()
ollama_endpoint = os.getenv("OLLAMA_ENDPOINT") # example: "http://localhost:11434/"
ollama_llm_name = os.getenv("OLLAMA_LLM") # example: "deepseek-r1:32b"
ollama_embed_name = os.getenv("OLLAMA_EMBED") # example: "all-minilm"

class Models:
    class AIModels(Enum):
        OLLAMA = "ollama"

    class EmbeddingModels(Enum):
        OLLAMA = "ollama"

    @abstractmethod
    def get_LLM(ai_model: AIModels, temperature: float = -1) -> Ollama:
        match ai_model:
            case Models.AIModels.OLLAMA:
                return Ollama(
                    base_url=ollama_endpoint,
                    model=ollama_llm_name,
                    request_timeout=1000.0
                )
            case _:
                raise ValueError("Unsupported AI model")


    @abstractmethod
    def get_embedding_model(ai_model: EmbeddingModels) -> OllamaEmbedding:
        if ai_model == Models.EmbeddingModels.OLLAMA:
            return OllamaEmbedding(
                        base_url= ollama_endpoint,
                        model_name=ollama_embed_name
                    )