import calendar
from datetime import date, timedelta

from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from firebase_auth.authentication import FirebaseAuthentication

from .models import Daily, Habit, Todo
from .permissions import IsOwnerOrReadOnly
from .serializers import (DailySerializer, HabitSerializer, TodoSerializer,
                          UserSerializer)

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

    return Response([serializer1.data, serializer2.data])


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)


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
        if 'reorder' in request.data:
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
        if 'reorder' in request.data:
            return reorder(self, Habit, HabitSerializer, request.data['reorder'])
        else:
            return self.update(request, *args, **kwargs)


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
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    serializer_class = DailySerializer
    permission_classes = is_authenticated_and_owner_classes
    authentication_classes = [SessionAuthentication, FirebaseAuthentication]

    def get_queryset(self):
        user = self.request.user
        habits = Habit.objects.filter(user=user)

        for habit in habits:
            Daily.objects.get_or_create(
                habit=habit, date=date.today(), user=user)

        if 'timeframe' in self.request.query_params:  # week, month, year
            obj_date = get_date(self.request.query_params)

            if self.request.query_params['timeframe'] == 'week':
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
