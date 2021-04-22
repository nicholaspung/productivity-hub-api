from rest_framework import serializers
from open_apps.models.app import App


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['title', 'id']
        read_only_fields = ['id', 'title', 'users']
