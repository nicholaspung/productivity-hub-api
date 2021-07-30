import logging

from open_apps.authentication import GeneralAuthentication
from open_apps.models.time_tracker import TrackTime, TrackTimeName, TimeTrackerPreferences
from open_apps.permissions import IsAuthenticatedAndOwner
from open_apps.serializers.time_tracker_serializers import (
    TrackTimeNameSerializer, TrackTimeSerializer, TimeTrackerPreferencesSerializer)
from open_apps.utils.api_utils import unused_method
from open_apps.utils.date_utils import get_date
from open_apps.utils.time_tracker_utils import get_archived_time_tracker_name_items, create_default_break_name
from open_apps.models.firebase_auth import Profile
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView

logger = logging.getLogger(__file__)


class TrackTimeNameViewSet(viewsets.ModelViewSet):
    """
    This view provides the `list`, `create`, `update`, and `delete` actions.
    """
    serializer_class = TrackTimeNameSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        is_archived = get_archived_time_tracker_name_items(self.request)
        create_default_break_name(self.request)
        return TrackTimeName.objects.filter(user=self.request.user, archived=is_archived)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request):
        return unused_method()


class TrackTimeViewSet(viewsets.ModelViewSet):
    """
    This view provides the `list`, `create`, `update`, and `delete` actions.
    """
    serializer_class = TrackTimeSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        obj_date = get_date(self.request.query_params)
        return TrackTime.objects.filter(user=self.request.user, date=obj_date)

    def perform_create(self, serializer):
        track_time_name_id = self.request.data.get('track_time_name')
        track_time_name_obj = TrackTimeName.objects.get(pk=track_time_name_id)
        if track_time_name_obj.user != self.request.user:
            track_time_name_obj = None
        serializer.save(user=self.request.user,
                        track_time_name=track_time_name_obj)

    def retrieve(self, request):
        return unused_method()


class TimeTrackerPreferencesAPIView(UpdateAPIView):
    serializer_class = TimeTrackerPreferencesSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return TimeTrackerPreferences.objects.filter(profile=profile)
