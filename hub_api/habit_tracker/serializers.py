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
        fields = ['date', 'finished', 'user', 'habit']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    habits = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='habit-detail')
    todos = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='todo-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'url', 'habits', 'todos']
