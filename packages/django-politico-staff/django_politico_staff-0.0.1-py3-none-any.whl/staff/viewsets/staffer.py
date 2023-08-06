from django.contrib.auth.models import User
from rest_framework.viewsets import ReadOnlyModelViewSet

from staff.serializers import UserSerializer


class StafferViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=True)
        is_active = self.request.query_params.get("active", None) in [
            "true",
            "1",
        ]
        if is_active:
            queryset = queryset.filter(is_active=True)
        return queryset
