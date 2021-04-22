from django.contrib.auth import get_user_model
from open_apps.models.firebase_auth import (Profile, UserAnalytic,
                                            UserAnalyticThreshold)
from open_apps.serializers.app_serializers import AppSerializer
from rest_framework import serializers
from open_apps.models.app import APPS
from open_apps.models.time_tracker import TimeTrackerPreferences
from open_apps.serializers.time_tracker_serializers import TimeTrackerPreferencesSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        read_only_fields = ['id', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_anonymous', 'apps', 'id', 'email']
        read_only_fields = ['id', 'user', 'email']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['apps'] = AppSerializer(instance.apps, many=True).data
        ret['app_preferences'] = {}
        for app in ret['apps']:
            if app['title'] == APPS[3]:  # Time Tracker
                time_tracker_preferences, _ = TimeTrackerPreferences.objects.get_or_create(
                    profile=instance)
                time_tracker_serialized = TimeTrackerPreferencesSerializer(
                    time_tracker_preferences).data
                ret['app_preferences']['time_tracker'] = time_tracker_serialized
        return ret


class UserAnalyticThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalyticThreshold
        fields = ['id', 'label', 'threshold']
        read_only_fields = ['id', 'user']


class UserAnalyticSerializer(serializers.ModelSerializer):
    threshold = UserAnalyticThresholdSerializer(many=False, read_only=True)

    class Meta:
        model = UserAnalytic
        fields = ['id', 'label', 'frequency',
                  'date', 'action', 'threshold']
        read_only_fields = ['id', 'user', 'date', 'label']
