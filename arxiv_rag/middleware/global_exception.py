from json import JSONDecodeError
from enum import Enum
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template import TemplateDoesNotExist
from django.conf import settings
from torch import OutOfMemoryError

"""
1. 1xx (Informational)
2. 2xx (Successful)
3. 3xx (Redirection)
4. 4xx (Client Error)
5. 5xx (Server Error)
"""


class ErrorCode(int, Enum):
    """
    Enumeration of error codes.
    """
    FILE_DOES_NOT_EXIST = 404
    OUT_OF_MEMORY = 507
    INVALID_API = 422
    UNCATEGORIZED_EXCEPTION = 500


class GlobalExceptionMiddleware:
    """
    Middleware to handle global exceptions and return appropriate JSON responses.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the given response handler.

        Args:
            get_response (callable): The response handler.
        """

        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request and return the response.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse:
        """
        Process exceptions and return JSON responses based on the exception type.

        Args:
            request (HttpRequest): The HTTP request object.
            exception (Exception): The exception that was raised.

        Returns:
            JsonResponse: The JSON response with the error code and message.
        """

        if isinstance(exception, ObjectDoesNotExist):
            return JsonResponse({
                'code': 500,
                'result': "FILE DOES NOT EXIT"
            },
                status=404)
        elif isinstance(exception, OutOfMemoryError):
            return JsonResponse({
                'code': 500,
                'result': "OUT OF MEMORY"
            },
                status=507)
        elif (isinstance(exception, JSONDecodeError) or
              isinstance(exception, TemplateDoesNotExist)):
            return JsonResponse({
                'code': 500,
                'result': "INVALID API"
            },
                status=422)
        else:
            if not settings.DEBUG:
                return JsonResponse({
                    'code': 999,
                    'result': "UNCATEGORIZED_EXCEPTION"
                },
                    status=500)
