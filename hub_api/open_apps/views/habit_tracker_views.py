import logging
from datetime import date

from open_apps.authentication import GeneralAuthentication
from open_apps.models.habit_tracker import Daily, Habit, Todo
from open_apps.permissions import IsAuthenticatedAndOwner
from open_apps.serializers.habit_tracker_serializers import (DailySerializer,
                                                             HabitSerializer,
                                                             TodoSerializer)
from open_apps.utils.api_utils import unused_method
from open_apps.utils.date_utils import get_date
from open_apps.utils.habit_tracker_utils import (
    create_dailies_according_to_weekdays, get_timeframe_queryset, reorder,
    sanitize_habits_weekdays, get_excluded_todo_items)
from rest_framework import status, viewsets
from rest_framework.response import Response

logger = logging.getLogger(__file__)


class TodoViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `partial_update`, `update`,
    and `destroy` actions.

    data:
        'reorder': '2nd pk'
    """
    serializer_class = TodoSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        filter_obj = get_excluded_todo_items(self.request)
        if filter_obj:
            return Todo.objects.filter(user=self.request.user).exclude(**filter_obj)
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if 'reorder' in request.data:  # reorder: todo_id
            return reorder(self, Todo, TodoSerializer, request.data['reorder'])
        return self.update(request, *args, **kwargs)


class HabitViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `partial_update`, `update`,
    and `destroy` actions.

    data:
        'reorder': '2nd pk'
        'weekdays': ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    """
    serializer_class = HabitSerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if request.data.get('reorder'):  # reorder: habit_id
            return reorder(self, Habit, HabitSerializer, request.data['reorder'])
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data.get('weekdays'):
            sanitized_data = sanitize_habits_weekdays(request.data)
            return super().update(sanitized_data, *args, **kwargs)
        return super().update(request, *args, **kwargs)


class DailyViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `partial_update`, and `update` actions.

    query_params:
        'timeframe': ['day', 'week', 'month', 'year']
        'date': 'yyyy-mm-dd'
    """
    serializer_class = DailySerializer
    permission_classes = IsAuthenticatedAndOwner
    authentication_classes = GeneralAuthentication

    def get_queryset(self):
        if 'timeframe' in self.request.query_params:
            return get_timeframe_queryset(self.request)
        return Daily.objects.filter(user=self.request.user, date=date.today())

    def create(self, request, *args, **kwargs):
        user = self.request.user
        obj_date = get_date(self.request.query_params)
        create_dailies_according_to_weekdays(user=user, obj_date=obj_date)
        queryset = Daily.objects.filter(user=user, date=obj_date)
        serialized = DailySerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request):
        return unused_method()

    def destroy(self, request):
        return unused_method()
