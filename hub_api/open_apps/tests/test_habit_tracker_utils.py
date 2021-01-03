from django.test import TestCase
from rest_framework.response import Response
from rest_framework import status
from open_apps.models.habit_tracker import Todo, Habit, Daily
from open_apps.serializers.habit_tracker_serializers import TodoSerializer, HabitSerializer
from open_apps.utils import habit_tracker_utils, date_utils
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()
TEST_USERNAME = "testcase"
TEST_PASSWORD = "strong_password_123"


class FakeClass():
    def __init__(self, instance='hi'):
        self.instance = instance

    def get_object(self):
        return self.instance


class HabitTrackerUtilTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_reorder(self):
        todo1 = Todo(name="todo1", user=self.user)
        todo1.save()
        todo2 = Todo(name="todo2", user=self.user)
        todo2.save()

        self_obj = FakeClass(todo1)
        response = habit_tracker_utils.reorder(
            self_obj, Todo, TodoSerializer, todo2.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], todo1.name)
        self.assertEqual(response.data[1]["name"], todo2.name)

        habit1 = Habit(name="habit1", user=self.user)
        habit1.save()
        habit2 = Habit(name="habit2", user=self.user)
        habit2.save()

        self_obj = FakeClass(habit1)
        response2 = habit_tracker_utils.reorder(
            self_obj, Habit, HabitSerializer, habit2.id)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data[0]["name"], habit1.name)
        self.assertEqual(response2.data[1]["name"], habit2.name)

    def test_sanitize_habits_weekdays(self):
        data1 = {'weekdays': 'Sun,Mon,Tue,Wed,Thu,Fri,Sat'}
        response = habit_tracker_utils.sanitize_habits_weekdays(data1)
        self.assertEqual(response.data["weekdays"], data1['weekdays'])

        data2 = {'weekdays': 'Yar,MMon,Tue,Wed,Thu,Fri,Satd'}
        response2 = habit_tracker_utils.sanitize_habits_weekdays(data2)
        self.assertEqual(response2.data["weekdays"], 'Tue,Wed,Thu,Fri')

    def test_create_dailies_according_to_weekdays(self):
        habit1 = Habit(name="habit1", user=self.user, weekdays="Sat")
        habit1.save()
        habit2 = Habit(name="habit2", user=self.user, archived=True)
        habit2.save()
        date1 = date(2021, 1, 2)
        habit_tracker_utils.create_dailies_according_to_weekdays(
            self.user, date1)
        self.assertEqual(
            len(Daily.objects.filter(user=self.user, date=date1)), 1)

        date2 = date(2021, 1, 3)
        habit_tracker_utils.create_dailies_according_to_weekdays(
            self.user, date1)
        self.assertEqual(
            len(Daily.objects.filter(user=self.user, date=date2)), 0)

        habit2.archived = False
        habit2.save()
        date3 = date(2021, 1, 4)
        habit_tracker_utils.create_dailies_according_to_weekdays(
            self.user, date3)
        self.assertEqual(
            len(Daily.objects.filter(user=self.user, date=date3)), 1)

    def test_get_timeframe_queryset(self):
        habit = Habit(name="habit", user=self.user)
        habit.save()
        single_day = (date(2021, 1, 1), '2021-01-01')
        request = FakeClass()
        setattr(request, 'user', self.user)
        setattr(request, 'query_params', {
            'timeframe': 'day', 'date': single_day[1]})
        habit_tracker_utils.create_dailies_according_to_weekdays(
            self.user, single_day[0])
        response1 = habit_tracker_utils.get_timeframe_queryset(request)
        self.assertEqual(len(response1), 1)

        week_day = (date(2020, 12, 27), '2020-12-27')
        setattr(request, 'query_params', {
                'timeframe': 'week', 'date': week_day[1]})
        habit_tracker_utils.create_dailies_according_to_weekdays(
            self.user, week_day[0])
        response2 = habit_tracker_utils.get_timeframe_queryset(request)
        self.assertEqual(len(response2), 2)

        month_day = (date(2020, 12, 5), '2020-12-05')
        setattr(request, 'query_params', {
                'timeframe': 'month', 'date': month_day[1]})
        habit_tracker_utils.create_dailies_according_to_weekdays(
            self.user, month_day[0])
        response3 = habit_tracker_utils.get_timeframe_queryset(request)
        self.assertEqual(len(response3), 2)

        year_day = (date(2020, 1, 1), '2020-01-01')
        setattr(request, 'query_params', {
                'timeframe': 'year', 'date': year_day[1]})
        habit_tracker_utils.create_dailies_according_to_weekdays(
            self.user, year_day[0])
        response4 = habit_tracker_utils.get_timeframe_queryset(request)
        self.assertEqual(len(response4), 3)

        setattr(request, 'query_params', {})
        response5 = habit_tracker_utils.get_timeframe_queryset(request)
        self.assertEqual(len(response5), 0)

        habit_tracker_utils.create_dailies_according_to_weekdays(
            self.user, date.today())
        response6 = habit_tracker_utils.get_timeframe_queryset(request)
        self.assertEqual(len(response6), 1)
