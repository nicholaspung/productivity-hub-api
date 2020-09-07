from rest_framework import serializers
from .models import Todo, Habit, Daily
from django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
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


class UserSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True)
    todos = TodoSerializer(many=True, read_only=True)
    dailies = DailySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'url', 'habits', 'todos', 'dailies']
