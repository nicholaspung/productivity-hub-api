from django.contrib.auth import get_user_model
from open_apps.models.firebase_auth import Profile, UserAnalytic, ViceThreshold
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'is_anonymous', 'apps']
        read_only_fields = ['id']


class ViceThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViceThreshold
        fields = ['id', 'user', 'label', 'threshold']
        read_only_fields = ['id', 'user']


class UserAnalyticSerializer(serializers.ModelSerializer):
    threshold = ViceThresholdSerializer(many=False, read_only=True)

    class Meta:
        model = UserAnalytic
        fields = ['id', 'user', 'label', 'frequency',
                  'date', 'action', 'threshold']
        read_only_fields = ['id', 'user', 'date', 'label']
