
from django.urls import include, path
from rest_framework import routers

from .viewsets import StafferViewSet

router = routers.DefaultRouter()

router.register(r"staffer", StafferViewSet, basename="staffer")

urlpatterns = [path("api", include(router.urls))]
