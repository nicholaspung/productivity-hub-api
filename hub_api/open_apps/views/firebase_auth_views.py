from django.http import Http404
from open_apps.authentication import GeneralAuthentication
from open_apps.models.firebase_auth import UserAnalytic, ViceThreshold, Profile
from open_apps.permissions import IsAuthenticatedAndOwner
from open_apps.serializers.firebase_auth_serializers import (
    ProfileSerializer, UserAnalyticSerializer, UserSerializer)
from open_apps.utils.firebase_auth_utils import (
    create_user_analytic, create_vice_threshold, delete_firebase_user,
    increment_user_analytic_frequency)
from open_apps.utils.date_utils import get_date, get_week_range
from rest_framework import status, viewsets
from rest_framework.generics import DestroyAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from open_apps.utils.api_utils import unused_method

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
        delete_firebase_user(self)
        return super().destroy(self, request, *args, **kwargs)


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
        week_dates = get_week_range(obj_date.year, isocalendar)
        return UserAnalytic.objects.filter(user=self.request.user, date__range=(
            week_dates[0], week_dates[1])).order_by('id')

    def create(self, request):
        obj_date = get_date(self.request.query_params)
        user = self.request.user
        labels = ["Post Saver Nav", "Saved Post Title",
                  "Saved Post Refresh", "All Post Title", "All Post Refresh"]
        for label in labels:
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
        incremented = increment_user_analytic_frequency(self)
        if incremented:
            return Response({'message': 'Analytics incremented.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Analytics created.'}, status=status.HTTP_201_CREATED)
