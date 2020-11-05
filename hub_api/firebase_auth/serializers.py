from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, UserAnalytic


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'is_anonymous', 'apps']


class UserAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalytic
        fields = ['id', 'user', 'label', 'frequency', 'date', 'action']
        read_only_fields = ['id', 'user', 'date', 'label']
