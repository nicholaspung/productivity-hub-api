from open_apps.models.vice import Vice, ViceAnalytic, ViceThreshold
from rest_framework import serializers


class ViceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vice
        fields = ['id', 'user', 'name', 'link', 'archived']
        read_only_fields = ['id', 'user']


class ViceAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViceAnalytic
        fields = ['id', 'frequency', 'date',
                  'vice', 'threshold', 'last_updated']
        read_only_fields = ['id', 'user', 'threshold', 'vice']
        depth = 1


class ViceThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViceThreshold
        fields = ['id', 'user', 'name', 'threshold']
        read_only_fields = ['id', 'user']
