import re
from typing_extensions import override
from langchain_core.output_parsers import StrOutputParser

class AnswerOutputParser(StrOutputParser):
    @override
    def parse(self, text: str) -> str:
        return self.extract_anwser(text)

    def extract_anwser(self, output: str) -> str:
        pattern = r"### Trả lời :\n(.*)"
        match = re.search(pattern, output, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return output