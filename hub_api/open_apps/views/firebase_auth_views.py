from django.contrib.auth import get_user_model
from django.http import Http404
from open_apps.authentication import GeneralAuthentication
from open_apps.models.firebase_auth import (LABELS, Profile, UserAnalytic,
                                            ViceThreshold)
from open_apps.permissions import IsAuthenticatedAndOwner
from open_apps.serializers.firebase_auth_serializers import (
    ProfileSerializer, UserAnalyticSerializer, UserSerializer,
    ViceThresholdSerializer)
from open_apps.utils.api_utils import unused_method
from open_apps.utils.date_utils import get_date, get_week_range
from open_apps.utils.firebase_auth_utils import (
    create_user_analytic, create_vice_threshold, delete_firebase_user,
    increment_user_analytic_frequency)
from rest_framework import status, viewsets
from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.response import Response

User = get_user_model()


class UserAPIView(DestroyAPIView):
    """
    This view provides the `destroy` action.
    """
    serializer_class = UserSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def destroy(self, request, *args, **kwargs):
        delete_firebase_user(self.request.user)
        return super().destroy(request, *args, **kwargs)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This view provides the `list` and `partial_update` actions.
    """
    serializer_class = ProfileSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def list(self, request):
        profile = Profile.objects.get(user=self.request.user)
        serialized = ProfileSerializer(profile)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request):
        return unused_method()

    def destroy(self, request):
        return unused_method()

    def create(self, request, *args, **kwargs):
        return unused_method()


class UserAnalyticAPIView(ListCreateAPIView):
    """
    This viewset provides `list`, `create` actions.

    query_params:
        'date': 'yyyy-mm-dd'

    data:
        'label': str
    """
    serializer_class = UserAnalyticSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        obj_date = get_date(self.request.query_params)
        isocalendar = obj_date.isocalendar()
        week_dates = get_week_range(isocalendar)
        return UserAnalytic.objects.filter(user=self.request.user, date__range=(
            week_dates[0], week_dates[1])).order_by('id')

    def create(self, request):
        obj_date = get_date(self.request.query_params)
        user = self.request.user
        for label in LABELS:
            try:
                ua_threshold = ViceThreshold.objects.get(
                    user=user, label=label)
            except ViceThreshold.DoesNotExist:
                try:
                    ua_threshold = create_vice_threshold(
                        user=user, label=label)
                except Exception:
                    raise Http404('Something went wrong.') from None
            create_user_analytic(user=user, label=label,
                                 obj_date=obj_date, threshold=ua_threshold)
        incremented = increment_user_analytic_frequency(self.request)
        if incremented:
            return Response({'message': 'Analytics incremented.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Analytics created.'}, status=status.HTTP_201_CREATED)


class ViceThresholdViewset(viewsets.ModelViewSet):
    """
    This viewset provides `create` and `update` action.

    data:
        'threshold': int
        'label': str
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
        # Check if label is correct
        label = self.request.data.get('label', None)
        if label not in LABELS:
            return Response({'message': 'Label not found.'}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)

        try:
            u_a_objs = UserAnalytic.objects.filter(
                label=label, user=user).order_by('-date')
            u_a = u_a_objs[0]  # Latest user analytic
            new_v_t = ViceThreshold.objects.get(pk=response.data["id"])
            u_a.threshold = new_v_t
            u_a.save()
        except:
            response.data['message'] = 'Unable to attach newly created ViceThreshold to UserAnalytic.'
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response

        return response

    def retrieve(self, request):
        return unused_method()

    def list(self, request):
        return unused_method()

    def destroy(self, request):
        return unused_method()
