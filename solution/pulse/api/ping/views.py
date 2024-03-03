from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PingApiView(APIView):
    def get(self, request):
        data = {"message": "ok"}
        return Response(data, status=status.HTTP_200_OK)
