import os

from llama_index.vector_stores.lancedb import LanceDBVectorStore


# gives vectore store object with specific table
def get_vector_store(table_name: str = "", mode: str = "read") -> None | LanceDBVectorStore:
    if (table_name == ""):
        return None
    
    env_dir = os.getenv("PROJECT_ENVIRONMENT")
    uri = f"./DB_FILES/{env_dir if env_dir is not None else 'DEV'}/{table_name}"

    return LanceDBVectorStore(
        uri=uri, mode=mode, query_type="vector"
    )