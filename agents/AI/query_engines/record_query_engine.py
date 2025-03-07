import logging as log
from typing import List

from llama_cloud import FilterOperator, MetadataFilter, MetadataFilters
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo
from llama_index.core.schema import BaseNode, IndexNode, NodeWithScore
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.vector_stores.lancedb.base import LanceDBVectorStore

from db.vector_db import get_vector_store
from AI.models import Models


class RecordQueryTool():
    def __init__(self):
        self.llm = Models.get_LLM(Models.AIModels.OLLAMA)
        self.embed_model = Models.get_embedding_model(Models.EmbeddingModels.OLLAMA)

    def get_records(self, table_name: str, question: str):
        try:
            vector_store_info = VectorStoreInfo(
                content_info="User records",
                metadata_info=[
                    MetadataInfo(
                        name="summary",
                        description="summary of the record",
                        type="string"
                    ),
                    MetadataInfo(
                        name="upload_year",
                        description="year in which record was uploaded on system",
                        type="Integer"
                    ),
                    MetadataInfo(
                        name="upload_month",
                        description="month in which record was uploaded on system",
                        type="Integer"
                    ),
                    MetadataInfo(
                        name="upload_day",
                        description="day in which record was uploaded on system",
                        type="Integer"
                    ),
                ]
            )

            vector_store: None | LanceDBVectorStore = get_vector_store(table_name, "read")

            vector_index: VectorStoreIndex = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=self.embed_model)

            data_nodes: List[BaseNode] = vector_store.get_nodes()

            indexed_nodes = []

            for doc in data_nodes:
                index_node = IndexNode(
                    text=doc.to_dict()["metadata"]["summary"],
                    metadata=doc.metadata,
                    index_id=doc.id_,
                )

                indexed_nodes.append(index_node)

            # Since "index_nodes" are concise summaries, we can directly feed them as objects into VectorStoreIndex
            index = VectorStoreIndex(objects=indexed_nodes, embed_model=self.embed_model)

            retriever = VectorIndexAutoRetriever(
                index=index,
                vector_store_info=vector_store_info,
                similarity_top_k=10,
                empty_query_top_k=10,  # if only metadata filters are specified, this is the limit
                verbose=True,
                llm=self.llm
            )

            nodes: List[NodeWithScore] = retriever.retrieve(question)

            return nodes

        except Exception as e:
            log.error("error on getting records, from RecordQueryTool")
            log.error(e)
            return []


record_query_tool = RecordQueryTool()