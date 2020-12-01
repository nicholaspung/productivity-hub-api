import calendar
from datetime import date, timedelta
from types import SimpleNamespace

from open_apps.authentication import FirebaseAuthentication
from open_apps.models.habit_tracker import (ENUM_PRIORITY_CHOICES, Daily,
                                            Habit, Todo)
from open_apps.permissions import IsOwnerOrReadOnly
from open_apps.serializers.habit_tracker import (DailySerializer,
                                                 HabitSerializer,
                                                 TodoSerializer)
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

is_authenticated_and_owner_classes = [
    permissions.IsAuthenticated, IsOwnerOrReadOnly]


def get_date(data):
    if 'date' in data:  # 2020-09-08 | YYYY-MM-DD
        request_date = data["date"]
        return date(int(request_date[:4]), int(
            request_date[5:7]), int(request_date[-2:]))

    return date.today()


def reorder(self, Model, ModelSerializer, id):
    model1 = self.get_object()
    model2 = Model.objects.get(pk=id)

    model1.order, model2.order = model2.order, model1.order

    model1.save()
    model2.save()

    serializer1 = ModelSerializer(model1)
    serializer2 = ModelSerializer(model2)

    return Response([serializer1.data, serializer2.data], status=status.HTTP_200_OK)


class TodoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = TodoSerializer
    permission_classes = is_authenticated_and_owner_classes
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if 'reorder' in request.data:  # reorder: todo_id
            return reorder(self, Todo, TodoSerializer, request.data['reorder'])
        else:
            return self.update(request, *args, **kwargs)


class HabitViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = HabitSerializer
    permission_classes = is_authenticated_and_owner_classes
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if request.data.get('reorder'):  # reorder: habit_id
            return reorder(self, Habit, HabitSerializer, request.data['reorder'])
        else:
            return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request_data_copy = request.data.copy()
        if request_data_copy.get('weekdays'):
            weekday_names = {'Sun': 'Sun', 'Mon': 'Mon', 'Tue': 'Tue',
                             'Wed': 'Wed', 'Thu': 'Thu', 'Fri': 'Fri', 'Sat': 'Sat'}
            current_weekdays = request_data_copy['weekdays']
            filtered_current_weekdays = [
                day for day in current_weekdays.split(',') if bool(weekday_names.get(day))]
            request_data_copy['weekdays'] = ','.join(filtered_current_weekdays)
            request_data_copy = {'data': request_data_copy}
            ns = SimpleNamespace(**request_data_copy)
            return super().update(ns, *args, **kwargs)
        else:
            return super().update(request, *args, **kwargs)


def week__range(year, isoCalendar):
    isoCalendarMonth = isoCalendar[1]
    if isoCalendar[2] == 7:
        isoCalendarMonth += 1
    return (date.fromisocalendar(year, isoCalendarMonth, 1) - timedelta(days=1), date.fromisocalendar(year, isoCalendarMonth, 1) + timedelta(days=5))


def month_range(year, month):
    return (date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1]))


def year_range(year):
    return (date(year, 1, 1), date(year, 12, 31))


class DailyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, and `update` actions.
    """
    serializer_class = DailySerializer
    permission_classes = is_authenticated_and_owner_classes
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        if 'timeframe' in self.request.query_params:  # week, month, year
            obj_date = get_date(self.request.query_params)
            if self.request.query_params['timeframe'] == 'day':
                queryset = Daily.objects.filter(
                    user=self.request.user, date=obj_date)
            elif self.request.query_params['timeframe'] == 'week':
                isocalendar = obj_date.isocalendar()
                week_dates = week__range(obj_date.year, isocalendar)
                queryset = Daily.objects.filter(user=self.request.user, date__range=(
                    week_dates[0], week_dates[1]))
            elif self.request.query_params['timeframe'] == 'month':
                month_dates = month_range(obj_date.year, obj_date.month)
                queryset = Daily.objects.filter(user=self.request.user, date__range=(
                    month_dates[0], month_dates[1]))
            elif self.request.query_params['timeframe'] == 'year':
                year_dates = year_range(obj_date.year)
                queryset = Daily.objects.filter(user=self.request.user,
                                                date__range=(year_dates[0], year_dates[1]))
            else:
                queryset = Daily.objects.filter(
                    user=self.request.user, date=date.today())
        else:
            queryset = Daily.objects.filter(
                user=self.request.user, date=date.today())
        return queryset

    def create(self, serializer):
        user = self.request.user
        habits = Habit.objects.filter(user=user, archived=False)
        obj_date = get_date(self.request.query_params)

        for habit in habits:
            weekday_values = {6: 'Sun', 0: 'Mon', 1: 'Tue',
                              2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat'}
            current_weekday = obj_date.weekday()
            if weekday_values[current_weekday] in habit.weekdays.split(','):
                Daily.objects.get_or_create(
                    habit=habit, date=obj_date, user=user)

        queryset = Daily.objects.filter(user=user, date=obj_date)
        serialized = DailySerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        response = {'message': 'Detail function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
