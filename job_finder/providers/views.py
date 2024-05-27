from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from providers.tasks import get_provider_results_in_bulk


class TestAPIView(APIView):  # TODO: REMOVE ME
    def get(self, request, format=None):
        if settings.DEBUG:
            get_provider_results_in_bulk()
        return Response()
