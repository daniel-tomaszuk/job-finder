from rest_framework.response import Response
from rest_framework.views import APIView

from providers.controllers import IndeedScrapperController


class TestAPIView(APIView):  # TODO: REMOVE ME
    def get(self, request, format=None):
        IndeedScrapperController().get_results()
        return Response()
