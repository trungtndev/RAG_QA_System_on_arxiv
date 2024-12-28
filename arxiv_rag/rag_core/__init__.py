from django.conf import settings
from langchain_core.runnables.passthrough import RunnablePassthrough

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore

from qdrant_client import QdrantClient
from qdrant_client.models import (VectorParams,
                                  Distance,
                                  SparseVectorParams,
                                  )
from .output_parser import AnswerOutputParser

CLIENT = QdrantClient(**settings.DATABASES["qdrant"])
if not CLIENT.collection_exists("pdf_collection"):
    CLIENT.create_collection(
        collection_name=settings.RAG_CONFIG["QDRANT_VECTORSTORE"]["collection_name"],
        vectors_config={
            "dense": VectorParams(size=768, distance=Distance.COSINE),
        },
        sparse_vectors_config={
            "sparse": SparseVectorParams(),
        }
    )

DENSE_EMBEDDING = HuggingFaceEmbeddings(**settings.RAG_CONFIG["DENSE_EMBEDDING"])
SPARSE_EMBEDDING = FastEmbedSparse(**settings.RAG_CONFIG["SPARSE_EMBEDDING"])
LLM = HuggingFacePipeline.from_model_id(**settings.RAG_CONFIG["LLM"])

VECTOR_STORE = QdrantVectorStore(
    client=CLIENT,
    embedding=DENSE_EMBEDDING,
    sparse_embedding=SPARSE_EMBEDDING,
    **settings.RAG_CONFIG["QDRANT_VECTORSTORE"]
)
RETRIEVER = VECTOR_STORE.as_retriever(**settings.RAG_CONFIG["RETRIEVER"])

CHAIN = ({"context": RETRIEVER, "question": RunnablePassthrough()}
         | LLM
         | AnswerOutputParser()
         )