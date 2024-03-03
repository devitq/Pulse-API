from django.http import JsonResponse
from rest_framework import status


class ErrorResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= status.HTTP_400_BAD_REQUEST:
            response.data = {"reason": response.data}
            response = JsonResponse(response.data, status=response.status_code)
        return response
