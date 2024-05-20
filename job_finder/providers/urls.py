from django.urls import path

from providers.views import TestAPIView

urlpatterns = [
    path("test-1/", TestAPIView.as_view()),
]
