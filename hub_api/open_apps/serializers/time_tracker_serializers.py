from re import T
from open_apps.models.time_tracker import TrackTime, TrackTimeName, TimeTrackerPreferences
from rest_framework import serializers


class TrackTimeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackTimeName
        fields = ['id', 'name', 'archived']
        read_only_fields = ['id', 'user']


class TrackTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackTime
        fields = ['id', 'date', 'track_time_name', 'start_time',
                  'end_time', 'total_time']
        read_only_fields = ['id', 'user', 'total_time']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['track_time_name'] = TrackTimeNameSerializer(
            instance.track_time_name).data
        return ret


class TimeTrackerPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTrackerPreferences
        fields = ['id', 'enable_pomodoro',
                  'pomodoro_interval_time', 'break_interval_time']
        read_only_fields = ['id', 'user']
