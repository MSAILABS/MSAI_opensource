import logging as log
from typing import List

from llama_index.core import VectorStoreIndex

from llama_index.core.schema import BaseNode, Document
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core.base.base_query_engine import BaseQueryEngine

from db.vector_db import get_vector_store


# always make sure that both embed model and llm model are same type
embed_model = Models.get_embedding_model(Models.EmbeddingModels.GPT4)
llm = Models.get_LLM(Models.AIModels.GPT4)

def add_data_into_vector_store(record_id: str, table_name: str, doc: Document) -> bool:
    isSaved = False
    try:
        vector_store: None | LanceDBVectorStore = get_vector_store(table_name, "append")

        index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)

        index.insert(document=doc)

        isSaved = True
    except ValueError as e:
        vector_store: None | LanceDBVectorStore = get_vector_store(table_name, "overwrite")

        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, 
            embed_model=embed_model,
            
        )

        index.insert(doc)

        isSaved = True
    except Exception as e:
        log.error("error on saving data into vector db")
        log.error(e)
        isSaved = False
    finally:
        return isSaved
    

def query_from_vector_store(table_name: str, query: str) -> str:
    try:
        vector_store: None | LanceDBVectorStore = get_vector_store(table_name, "read")

        index: VectorStoreIndex = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)

        query_engine: BaseQueryEngine = index.as_query_engine(llm=llm)

        response = query_engine.query(query)

        return response.response
    except Exception as e:
        log.error("error on saving data into vector db")
        log.error(e)
        
        return "Error on querying."
    

def get_users_records_id(table_name: str) -> list[str]:
    try:
        ids = []
        vector_store: None | LanceDBVectorStore = get_vector_store(table_name, "read")

        nodes: List[BaseNode] = vector_store.get_nodes()

        for node in nodes:
            ids.append(node.metadata["record_id"])

        return ids
    except Exception as e:
        log.error("error on getring users records id from vector db")
        log.error(e)
        
        return []


def delete_user_record(table_name: str, record_id: str) -> bool:
    try:
        vector_store: None | LanceDBVectorStore = get_vector_store(table_name, "overwrite")

        nodes = vector_store.get_nodes()

        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, 
            embed_model=embed_model,
            
        )

        if nodes and len(nodes) > 0:
            for node in nodes:
                if node.metadata["record_id"] == record_id:
                    index.delete_ref_doc(node.ref_doc_id, delete_from_docstore=True)
                    return True

        return False
    except Exception as e:
        log.error("error on deleting user record from vector db")
        log.error(e)
        return False
