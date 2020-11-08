from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, UserAnalytic, ViceThreshold


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'is_anonymous', 'apps']


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
