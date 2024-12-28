from django.http import JsonResponse, HttpResponse, HttpRequest
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView

from typing import (
    Optional
)
from .services import DocumentService

"""
GET	    /docs/	        list	    
GET	    /docs/<id>/	    retrieve	
POST    /docs/	        create	    
PUT	    /docs/<id>/	    update	    
DELETE	/docs/<id>/	    destroy	    
"""


class DocumentView(ViewSet):
    manager_service = DocumentService()

    def create(self, request) -> HttpResponse:
        return self.manager_service.update_document(request)


    def list(self, request: HttpRequest) -> HttpResponse:
        return JsonResponse({})

    def retrieve(self, request: HttpRequest, id: Optional[str] = None) -> HttpResponse:
        return JsonResponse({})

    def update(self, request: HttpRequest, id: Optional[str] = None):
        return JsonResponse({})

    def destroy(self, request: HttpRequest, id: Optional[str] = None) -> HttpResponse:
        return JsonResponse({})

    def partial_update(self, request: HttpRequest, id: Optional[str] = None) -> HttpResponse:
        return JsonResponse({})
