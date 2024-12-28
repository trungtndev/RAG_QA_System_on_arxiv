
from django.conf import settings
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore

from qdrant_client import QdrantClient

from rag_core.output_parser import AnswerOutputParser
from rag_core.utils import format_documents

SYSTEM_PROMPT = """
Chú ý các yêu cầu sau:
- Câu trả lời phải chính xác và đầy đủ nếu ngữ cảnh có câu trả lời. 
- Chỉ sử dụng các thông tin có trong ngữ cảnh được cung cấp.
- Chỉ cần từ chối trả lời và không suy luận gì thêm nếu ngữ cảnh không có câu trả lời.
Hãy trả lời câu hỏi dựa trên ngữ cảnh:
### Ngữ cảnh :
{context}

### Câu hỏi :
{question}

### Trả lời :

"""
PROMPT = PromptTemplate(template=SYSTEM_PROMPT, input_variables=["context", "question"])

class RagService:
    def __init__(self, validate=True):
        self.client = QdrantClient(**settings.DATABASES["qdrant"])
        if validate:
            self._validate_collection(settings.RAG_CONFIG["QDRANT_VECTORSTORE"]["collection_name"])

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
        return ({"context": self.retriever | format_documents, "question": RunnablePassthrough()}
             | PROMPT
             | self.llm
             | AnswerOutputParser()
             )
    def _validate_collection(self, collection_name):
        from qdrant_client.models import (VectorParams,
                                          Distance,
                                          SparseVectorParams,
                                          )
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "dense": VectorParams(size=384, distance=Distance.COSINE),
                },
                sparse_vectors_config={
                    "sparse": SparseVectorParams(),
                }
            )
        return collection_name