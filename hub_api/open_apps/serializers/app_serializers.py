from rest_framework import serializers
from open_apps.models.app import App
from open_apps.serializers.firebase_auth_serializers import ProfileSerializer


class AppSerializer(serializers.ModelSerializer):
    users = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = App
        fields = ['title']
        read_only_fields = ['id', 'title']
