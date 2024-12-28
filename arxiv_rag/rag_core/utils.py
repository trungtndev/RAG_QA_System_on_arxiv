from langchain_core.runnables.base import Runnable, RunnableMap, chain
from langchain_core.documents import Document
from typing import List
import re

@chain
def remove_links(text: str) -> str:
    url_pattern = r"https?://\S+|www\.\S+"
    return re.sub(url_pattern, "", text)

@chain
def format_documents(documents: List[Document]) -> str:
    texts = []
    for doc in documents:
        texts.append(doc.page_content)
        texts.append("---")

    return "\n".join(texts)