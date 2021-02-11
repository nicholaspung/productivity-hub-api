from types import SimpleNamespace

from open_apps.authentication import GeneralAuthentication
from open_apps.models.vice import Vice, ViceAnalytic
from open_apps.permissions import IsAuthenticatedAndOwner
from open_apps.serializers.vice_serializers import (ViceAnalyticSerializer,
                                                    ViceSerializer)
from open_apps.utils.api_utils import unused_method
from open_apps.utils.date_utils import get_date
from open_apps.utils.vice_utils import create_unarchived_vice_analytics
from rest_framework import status, viewsets
from rest_framework.response import Response


class ViceViewSet(viewsets.ModelViewSet):
    """
    This view provides the `retrieve`, `create`, `update`, and `delete` actions.
    """
    serializer_class = ViceSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        return Vice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        return unused_method()


class ViceAnalyticViewSet(viewsets.ModelViewSet):
    """
    This view provides the `create` and `update` actions.
    """
    serializer_class = ViceAnalyticSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        obj_date = get_date(self.request.query_params)
        return ViceAnalytic.objects.filter(user=self.request.user, date=obj_date)

    def create(self, request, *args, **kwargs):
        obj_date = get_date(self.request.query_params)
        user = self.request.user
        create_unarchived_vice_analytics(user, obj_date)

        vice_analytics = ViceAnalytic.objects.filter(user=user, date=obj_date)
        serialized = ViceAnalyticSerializer(vice_analytics, many=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        return unused_method()

    def list(self, request):
        return unused_method()
