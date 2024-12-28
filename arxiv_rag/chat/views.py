from django.http import JsonResponse, HttpResponse, HttpRequest
from rest_framework.viewsets import ViewSet
from typing import (
    Optional
)
from .services import ChatService

"""
GET	    /chat/	        list	    
GET	    /chat/<id>/	    retrieve	
POST    /chat/	        create	    
PUT	    /chat/<id>/	    update	    
DELETE	/chat/<id>/	    destroy	    
"""


class ChatView(ViewSet):

    manager_service = ChatService()

    def create(self, request) -> HttpResponse:
        self.manager_service.chat(request)
        return JsonResponse({})

    def list(self, request: HttpRequest) -> HttpResponse:
        return JsonResponse({})

    def retrieve(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        return JsonResponse({})

    def update(self, request: HttpRequest, pk: Optional[str] = None):
        return JsonResponse({})

    def destroy(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        return JsonResponse({})

    def partial_update(self, request: HttpRequest, pk: Optional[str] = None) -> HttpResponse:
        return JsonResponse({})
