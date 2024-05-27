from rest_framework.response import Response
from rest_framework.views import APIView

from providers.controllers import IndeedScrapperController
from providers.models import Provider
from providers.tasks import get_provider_results
from scrapping_process.data_migrations.load_initial_data import LoadInitialDataMigration


class TestAPIView(APIView):  # TODO: REMOVE ME
    def get(self, request, format=None):
        get_provider_results.delay()
        return Response()
