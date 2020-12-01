from open_apps.models.habit_tracker import (ENUM_PRIORITY_CHOICES, Daily,
                                            Habit, Todo)
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name', 'description', 'date_created',
                  'date_finished', 'finished', 'priority', 'user', 'order']
        read_only_fields = ['user', 'id', 'date_created', 'date_finished']


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description',
                  'date_created', 'order', 'user', 'archived', 'weekdays']
        read_only_fields = ['user', 'id', 'date_created']


class DailySerializer(serializers.ModelSerializer):
    habit = HabitSerializer(many=False, read_only=True)

    class Meta:
        model = Daily
        fields = ['id', 'date', 'finished', 'user', 'habit']
        read_only_fields = ['user', 'id', 'date', 'habit']
