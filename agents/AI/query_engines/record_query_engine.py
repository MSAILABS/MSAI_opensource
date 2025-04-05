import logging as log
from typing import List

from llama_cloud import FilterOperator, MetadataFilter, MetadataFilters
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo
from llama_index.core.schema import BaseNode, IndexNode, NodeWithScore
from llama_index.core import VectorStoreIndex
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.vector_stores.lancedb.base import LanceDBVectorStore

from db.vector_db import get_vector_store
from AI.models import Models, llm_model, embedding_model


class RecordQueryTool():
    def __init__(self):
        self.llm = Models.get_LLM(llm_model)
        self.embed_model = Models.get_embedding_model(embedding_model)

    def get_records(self, table_name: str, question: str, number_of_chunks_to_retrive):
        try:
            vector_store: None | LanceDBVectorStore = get_vector_store(table_name, "read")

            vector_index: VectorStoreIndex = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=self.embed_model)

            query_engine: BaseQueryEngine = vector_index.as_query_engine(llm=self.llm, similarity_top_k=number_of_chunks_to_retrive)

            nodes: List[NodeWithScore] = query_engine.retrieve(question)

            return nodes
        except Exception as e:
            log.error("error on getting records, from RecordQueryTool")
            log.error(e)
            return []


record_query_tool = RecordQueryTool()