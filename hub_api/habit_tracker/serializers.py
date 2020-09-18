from rest_framework import serializers

from .models import ENUM_PRIORITY_CHOICES, Daily, Habit, Todo


class TodoSerializer(serializers.ModelSerializer):
    priority = serializers.ChoiceField(
        choices=ENUM_PRIORITY_CHOICES, default=ENUM_PRIORITY_CHOICES[0])

    class Meta:
        model = Todo
        fields = ['id', 'name', 'description', 'date_created',
                  'date_finished', 'finished', 'priority', 'user', 'order']
        read_only_fields = ['user']


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description',
                  'date_created', 'order', 'user', 'archived']
        read_only_fields = ['user']


class DailySerializer(serializers.ModelSerializer):
    habit = HabitSerializer(many=False, read_only=True)

    class Meta:
        model = Daily
        fields = ['id', 'date', 'finished', 'user', 'habit']
        read_only_fields = ['user']
