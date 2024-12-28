
from django.conf import settings
from langchain_core.runnables.passthrough import RunnablePassthrough

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore

from qdrant_client import QdrantClient
from qdrant_client.models import (VectorParams,
                                  Distance,
                                  SparseVectorParams,
                                  )
from rag_core.output_parser import AnswerOutputParser


class RagService:
    def __init__(self, validate=True):
        self.client = QdrantClient(**settings.DATABASES["qdrant"])
        if validate:
            self._validate_collection(**settings.RAG_CONFIG["QDRANT_VECTORSTORE"]["collection_name"])

        self.dense_embedding = HuggingFaceEmbeddings(**settings.RAG_CONFIG["DENSE_EMBEDDING"])
        self.sparse_embedding = FastEmbedSparse(**settings.RAG_CONFIG["SPARSE_EMBEDDING"])

        self.llm = HuggingFacePipeline.from_model_id(**settings.RAG_CONFIG["LLM"])

        self.db_store = QdrantVectorStore(
            client=self.client,
            embedding=self.dense_embedding,
            sparse_embedding=self.sparse_embedding,
            **settings.RAG_CONFIG["QDRANT_VECTORSTORE"]
        )
        self.retriever = self.db_store.as_retriever(**settings.RAG_CONFIG["RETRIEVER"])

    def add_docs(self, docs) -> list[str]:
        return self.db_store.add_documents(docs)

    def chat(self, query, **kwargs):
        return self.qa_chain.invoke(query)

    @property
    def qa_chain(self):
        return ({"context": self.retriever, "question": RunnablePassthrough()}
         | self.llm
         | AnswerOutputParser()
         )
    def _validate_collection(self, collection_name):
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "dense": VectorParams(size=768, distance=Distance.COSINE),
                },
                sparse_vectors_config={
                    "sparse": SparseVectorParams(),
                }
            )
        return collection_name