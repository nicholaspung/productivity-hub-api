from open_apps.models.vice import Vice, ViceAnalytic
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
                  'vice', 'last_updated', 'time_between']
        read_only_fields = ['id', 'user', 'vice']
        depth = 1
