from types import SimpleNamespace

from open_apps.authentication import GeneralAuthentication
from open_apps.models.vice import Vice, ViceAnalytic, ViceThreshold
from open_apps.permissions import IsAuthenticatedAndOwner
from open_apps.serializers.vice_serializers import (ViceAnalyticSerializer,
                                                    ViceSerializer,
                                                    ViceThresholdSerializer)
from open_apps.utils.api_utils import unused_method
from open_apps.utils.date_utils import get_date
from open_apps.utils.vice_utils import (attach_vice_threshold_to_analytic,
                                        create_vice_analytic)
from rest_framework import status, viewsets
from rest_framework.response import Response


class ViceViewSet(viewsets.ModelViewSet):
    """
    This view provides the `list`, `create`, `update`, and `delete` actions.
    """
    serializer_class = ViceSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        return Vice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ViceAnalyticViewSet(viewsets.ModelViewSet):
    """
    This view provides the `list`, `create`, and `update` actions.
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
        vices = Vice.objects.filter(user=user)
        for vice in vices:
            create_vice_analytic(vice, user, obj_date)

        vice_analytics = ViceAnalytic.objects.filter(user=user, date=obj_date)
        serialized = ViceAnalyticSerializer(vice_analytics, many=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        frequency = instance.frequency + 1
        request_replacement = {"data": {"frequency": frequency}}
        n_s = SimpleNamespace(**request_replacement)
        return super().partial_update(n_s, *args, **kwargs)


class ViceThresholdViewSet(viewsets.ModelViewSet):
    """
    create, update
    This viewset provides `create` and `update` action.

    data:
        'threshold': int
        'name': str
    """
    serializer_class = ViceThresholdSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        return ViceThreshold.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        name = self.request.data.get('name', None)

        response = super().create(request, *args, **kwargs)
        if name is None:
            return response

        try:
            attach_vice_threshold_to_analytic(user, name, response.data["id"])
        except:
            response.data['message'] = 'Unable to attach newly created ViceThreshold to ViceAnalytic.'
            response.status_code = status.HTTP_400_BAD_REQUEST

        return response

    def retrieve(self, request):
        return unused_method()

    def list(self, request):
        return unused_method()

    def destroy(self, request):
        return unused_method()
