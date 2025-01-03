from typing import List, Dict, Any
from django.conf import settings

from django.http import JsonResponse, HttpResponse, HttpRequest
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from .models import Document
from rag_app.signals import docs_signal


class DocumentService(object):
    def __init__(self):
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=128,
            add_start_index=True,
        )

    def update_document(self, request: HttpRequest) -> HttpResponse:
        uploaded_file = request.FILES.get('file')
        file_instance = Document(title=uploaded_file.name,
                                     file_path=uploaded_file,
                                     )
        file_instance.save()
        loader = PyPDFLoader(settings.BASE_DIR / file_instance.file_path.path)
        documents = loader.load()
        chunks = self.recursive_splitter.split_documents(documents)

        num_chunks = docs_signal.send(sender='docs', docs=chunks)[0][1]
        print(num_chunks)
        return JsonResponse({
            'code': 200,
            'result': {
                'num_chunks': num_chunks
            }
        })

