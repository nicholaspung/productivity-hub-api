from rest_framework import serializers
from open_apps.models.apps import Apps


class AppsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apps
        fields = ['title']
        read_only_fields = ['id', 'title']
