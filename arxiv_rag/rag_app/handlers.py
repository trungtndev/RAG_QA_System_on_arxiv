from django.dispatch import receiver
from .signals import rag_signal, docs_signal, chat_signal
from .services import RagService

rag_service = RagService()

@receiver(docs_signal)
def add_docs(sender, docs, **kwargs):
    result = rag_service.add_docs(docs)
    return result

@receiver(chat_signal)
def chat(sender, query, **kwargs):
    result = rag_service.chat(query)
    return result