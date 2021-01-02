from types import SimpleNamespace

from open_apps.models.habit_tracker import Daily, Habit
from open_apps.utils.date_utils import (get_date, get_month_range,
                                        get_week_range, get_year_range)
from rest_framework import status
from rest_framework.response import Response


def reorder(self, Model, ModelSerializer, model_id):
    model1 = self.get_object()
    model2 = Model.objects.get(pk=model_id)

    model1.order, model2.order = model2.order, model1.order

    model1.save()
    model2.save()

    serializer1 = ModelSerializer(model1)
    serializer2 = ModelSerializer(model2)

    return Response([serializer1.data, serializer2.data], status=status.HTTP_200_OK)


def sanitize_habits_weekdays(data):
    data_copy = data.copy()
    weekday_names = {'Sun': 'Sun', 'Mon': 'Mon', 'Tue': 'Tue',
                     'Wed': 'Wed', 'Thu': 'Thu', 'Fri': 'Fri', 'Sat': 'Sat'}
    current_weekdays = data_copy['weekdays']
    filtered_current_weekdays = [
        day for day in current_weekdays.split(',') if bool(weekday_names.get(day))]
    data_copy['weekdays'] = ','.join(filtered_current_weekdays)
    data_copy = {'data': data_copy}
    return SimpleNamespace(**data_copy)


def create_dailies_according_to_weekdays(user, obj_date):
    habits = Habit.objects.filter(user=user, archived=False)
    for habit in habits:
        weekday_values = {6: 'Sun', 0: 'Mon', 1: 'Tue',
                          2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat'}
        current_weekday = obj_date.weekday()
        if weekday_values[current_weekday] in habit.weekdays.split(','):
            Daily.objects.get_or_create(
                habit=habit, date=obj_date, user=user)


def get_timeframe_queryset(request):
    obj_date = get_date(request.query_params)
    timeframe = request.query_params['timeframe']
    user = request.user
    if timeframe == 'day':
        qs = Daily.objects.filter(user=user, date=obj_date)
    elif timeframe == 'week':
        isocalendar = obj_date.isocalendar()
        week_dates = get_week_range(isocalendar)
        qs = Daily.objects.filter(
            user=user, date__range=(week_dates[0], week_dates[1]))
    elif timeframe == 'month':
        month_dates = get_month_range(obj_date.year, obj_date.month)
        qs = Daily.objects.filter(
            user=user, date__range=(month_dates[0], month_dates[1]))
    elif timeframe == 'year':
        year_dates = get_year_range(obj_date.year)
        qs = Daily.objects.filter(
            user=user, date__range=(year_dates[0], year_dates[1]))
    else:
        qs = Daily.objects.filter(user=user, date=date.today())

    return qs
