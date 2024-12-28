from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from rag_app.signals import chat_signal


class ChatService(object):

    def chat(self, request: HttpRequest) -> HttpResponse:
        htpp2json = json.loads(request.body)

        question = htpp2json.get("message")
        answer = chat_signal.send(sender='chat', query=question)
        return JsonResponse({
            'code': 200,
            'result': {
                'answer': answer
            }
        })
