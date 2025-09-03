import os

from llama_index.vector_stores.lancedb import LanceDBVectorStore
from AI.models import embedding_model

def get_db_location(table_name: str):
    env_dir = os.getenv("PROJECT_ENVIRONMENT")
    uri = f"./DB_FILES/{env_dir if env_dir is not None else 'DEV'}/{embedding_model.name}/{table_name}"

    return uri


# gives vectore store object with specific table
def get_vector_store(table_name: str = "", mode: str = "read") -> None | LanceDBVectorStore:
    if (table_name == ""):
        return None
    
    uri = get_db_location(table_name=table_name)

    return LanceDBVectorStore(
        uri=uri, mode=mode, query_type="vector"
    )