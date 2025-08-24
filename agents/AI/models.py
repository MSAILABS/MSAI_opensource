from abc import abstractmethod
import os
from enum import Enum
from dotenv import load_dotenv

from llama_index.llms.ollama import Ollama
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding

# loading environment variables
load_dotenv()
gpt_embed_api_key = os.getenv("AZURE_HEALTHSCANNER_UK_EMBBED_SMALL_KEY")
gpt_embed_endpoint = os.getenv("AZURE_HEALTHSCANNER_UK_EMBBED_SMALL_ENDPOINT")
gpt_embed_version = os.getenv("AZURE_HEALTHSCANNER_UK_EMBBED_SMALL_VERSION")

print(f"embedding api key: {gpt_embed_api_key}")
print(f"embedding endpoint key: {gpt_embed_endpoint}")
print(f"embedding version key: {gpt_embed_version}")

ollama_endpoint = os.getenv("OLLAMA_ENDPOINT") # example: "http://localhost:11434/"
ollama_llm_name = os.getenv("OLLAMA_LLM") # example: "deepseek-r1:32b"
ollama_embed_name = os.getenv("OLLAMA_EMBED") # example: "all-minilm"

anthropic_llm_name = os.getenv("CLAUDE_LLM")
anthropic_api_key = os.getenv("CLAUDE_API_KEY")


class Models:
    class AIModels(Enum):
        DeepSeek = "DeepSeek"
        ANTHROPIC = "Claude"

    class EmbeddingModels(Enum):
        ALL_LLM_MINI = "all_lm_mini"
        OPENAI = "openai"
        MISTRAL = "avr/sfr-embedding-mistral"

    @abstractmethod
    def get_LLM(ai_model: AIModels, temperature: float = -1) -> Ollama:
        match ai_model:
            case Models.AIModels.DeepSeek:
                return Ollama(
                    base_url=ollama_endpoint,
                    model=ollama_llm_name,
                    request_timeout=1000.0
                )
            case Models.AIModels.ANTHROPIC:
                return Anthropic(
                    model=anthropic_llm_name,
                    api_key=anthropic_api_key
                )
            case _:
                raise ValueError("Unsupported AI model")


    @abstractmethod
    def get_embedding_model(embed_model: EmbeddingModels) -> OllamaEmbedding:
        match embed_model:
            case Models.EmbeddingModels.ALL_LLM_MINI | Models.EmbeddingModels.MISTRAL:
                return OllamaEmbedding(
                        base_url= ollama_endpoint,
                        model_name=ollama_embed_name
                    )
            case Models.EmbeddingModels.OPENAI:
                return AzureOpenAIEmbedding(
                        model="text-embedding-3-small",
                        deployment_name="text-embedding-3-small",
                        api_key=gpt_embed_api_key,
                        azure_endpoint=gpt_embed_endpoint,
                        api_version=gpt_embed_version,
                    )
        
llm_model = Models.AIModels.ANTHROPIC
embedding_model = Models.EmbeddingModels.OPENAI