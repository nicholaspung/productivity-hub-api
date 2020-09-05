from rest_framework import serializers
from .models import Todo, Habit, Daily
from django.contrib.auth.models import User


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ['name', 'description', 'date_created',
                  'date_finished', 'finished', 'priority', 'user', 'order']


class HabitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Habit
        fields = ['name', 'description',
                  'date_created', 'order', 'user', 'archived']


class DailySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Daily
        fields = ['date', 'habit', 'finished', 'user']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    habits = serializers.HyperlinkedRelatedField(
        many=True, view_name='habit-detail', read_only=True)
    todos = serializers.HyperlinkedRelatedField(
        many=True, view_name='todo-detail', read_only=True)
    dailies = serializers.HyperlinkedRelatedField(
        many=True, view_name='daily-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'url', 'habits', 'todos', 'dailies']
