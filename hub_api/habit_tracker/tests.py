import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Daily, Habit, Todo, ENUM_PRIORITY_CHOICES
from .serializers import (DailySerializer, HabitSerializer, TodoSerializer,
                          UserSerializer)
from .views import get_date

test_username = "testcase"
test_password = "strong_password_123"


# Integration Tests with API
class TodoTestCase(APITestCase):
    base_url = "/todos/"
    sample_todo = {"name": "new todo", "description": "new description"}

    def setUp(self):
        self.user = User.objects.create_user(
            username=test_username, password=test_password)
        self.client.login(username=test_username, password=test_password)

    def test_todo_create_view(self):
        response = self.client.post(self.base_url, data=self.sample_todo)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.sample_todo['name'])
        self.assertEqual(response.data['description'],
                         self.sample_todo['description'])

    def test_todo_list_view(self):
        self.client.post(self.base_url, data=self.sample_todo)
        todo2 = {"name": "new todo 2", "description": "new description 2"}
        self.client.post(self.base_url, data=todo2)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.sample_todo['name'])
        self.assertEqual(response.data[1]['name'], todo2['name'])
        self.assertEqual(
            response.data[0]['description'], self.sample_todo['description'])
        self.assertEqual(response.data[1]['description'], todo2['description'])

    def test_todo_detail_delete(self):
        self.client.post(self.base_url, data=self.sample_todo)
        response = self.client.delete(f"{self.base_url}1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_todo_detail_edit(self):
        self.client.post(self.base_url, data=self.sample_todo)
        # Edit name, description
        new_todo = {"name": "updated", "description": "updated"}
        response = self.client.put(f"{self.base_url}1/", data=new_todo)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_todo["name"])
        self.assertEqual(response.data["description"], new_todo["description"])
        # Edit finish status
        finished_field = {"finished": True, "name": new_todo["name"]}
        response2 = self.client.put(
            f"{self.base_url}1/", data=finished_field)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["finished"],
                         finished_field["finished"])
        finished_field["finished"] = False
        response3 = self.client.put(
            f"{self.base_url}1/", data=finished_field)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data["finished"],
                         finished_field["finished"])
        # Edit priority
        priority_field = {"priority": "high", "name": new_todo["name"]}
        response4 = self.client.put(f"{self.base_url}1/", data=priority_field)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.data["priority"],
                         priority_field["priority"])

    def test_todo_detail_order_switch(self):
        # Patch, data={reorder:id}
        self.client.post(self.base_url, data=self.sample_todo)
        todo = {"name": "yello", "description": "black"}
        self.client.post(self.base_url, data=todo)

        response = self.client.patch(f"{self.base_url}1/", data={"reorder": 2})
        # Id 1 has Order 1, Id 2 has Order 0
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.sample_todo["name"])
        self.assertEqual(response.data[0]["order"], 1)
        self.assertEqual(response.data[1]["name"], todo["name"])
        self.assertEqual(response.data[1]["order"], 0)

        new_todo = {"name": "blue", "description": "green"}
        self.client.post(self.base_url, data=new_todo)
        response2 = self.client.patch(
            f"{self.base_url}3/", data={"reorder": 1})
        # Id 3 has Order 1, Id 1 has Order 2
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data[0]["name"], new_todo["name"])
        self.assertEqual(response2.data[0]["order"], 1)
        self.assertEqual(response2.data[1]["name"], self.sample_todo["name"])
        self.assertEqual(response2.data[1]["order"], 2)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HabitTestCase(APITestCase):
    base_url = "/habits/"
    sample_habit = {"name": "new habit", "description": "new description"}

    def setUp(self):
        self.user = User.objects.create_user(
            username=test_username, password=test_password)
        self.client.login(username=test_username, password=test_password)

    def test_habit_create_view(self):
        response = self.client.post(self.base_url, data=self.sample_habit)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.sample_habit['name'])
        self.assertEqual(response.data['description'],
                         self.sample_habit['description'])

    def test_habit_list_view(self):
        self.client.post(self.base_url, data=self.sample_habit)
        habit2 = {"name": "new habit 2", "description": "new description 2"}
        self.client.post(self.base_url, data=habit2)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.sample_habit['name'])
        self.assertEqual(response.data[1]['name'], habit2['name'])
        self.assertEqual(
            response.data[0]['description'], self.sample_habit['description'])
        self.assertEqual(
            response.data[1]['description'], habit2['description'])

    def test_habit_detail_delete(self):
        self.client.post(self.base_url, data=self.sample_habit)
        response = self.client.delete(f"{self.base_url}1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_habit_detail_edit(self):
        self.client.post(self.base_url, data=self.sample_habit)
        # Edit name, description
        new_habit = {"name": "updated", "description": "updated"}
        response = self.client.put(f"{self.base_url}1/", data=new_habit)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_habit["name"])
        self.assertEqual(
            response.data["description"], new_habit["description"])
        # Edit archive status
        archived_field = {"archived": True, "name": self.sample_habit["name"]}
        response2 = self.client.put(
            f"{self.base_url}1/", data=archived_field)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["archived"],
                         archived_field["archived"])
        archived_field["archived"] = False
        response3 = self.client.put(
            f"{self.base_url}1/", data=archived_field)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data["archived"],
                         archived_field["archived"])

    def test_habit_detail_order_switch(self):
        # Patch, data={reorder:id}
        self.client.post(self.base_url, data=self.sample_habit)
        habit = {"name": "yello", "description": "black"}
        self.client.post(self.base_url, data=habit)

        response = self.client.patch(f"{self.base_url}1/", data={"reorder": 2})
        # Id 1 has Order 1, Id 2 has Order 0
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.sample_habit["name"])
        self.assertEqual(response.data[0]["order"], 1)
        self.assertEqual(response.data[1]["name"], habit["name"])
        self.assertEqual(response.data[1]["order"], 0)

        new_habit = {"name": "blue", "description": "green"}
        self.client.post(self.base_url, data=new_habit)
        response2 = self.client.patch(
            f"{self.base_url}3/", data={"reorder": 1})
        # Id 3 has Order 1, Id 1 has Order 2
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data[0]["name"], new_habit["name"])
        self.assertEqual(response2.data[0]["order"], 1)
        self.assertEqual(response2.data[1]["name"], self.sample_habit["name"])
        self.assertEqual(response2.data[1]["order"], 2)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


def create_sample_habit(name="new habit", description="new description"):
    return {"name": name, "description": description}


def create_sample_daily(habit, user, date):
    daily = Daily(habit=habit, user=user)
    daily.save()
    daily.date = get_date({"date": date})
    daily.save()


class DailyTestCase(APITestCase):
    base_url = "/dailies/"
    habit_url = '/habits/'

    def setUp(self):
        self.user = User.objects.create_user(
            username=test_username, password=test_password)
        self.client.login(username=test_username, password=test_password)

    def test_daily_list_view(self):
        habit1 = create_sample_habit()
        habit2 = create_sample_habit()
        self.client.post(self.habit_url, data=habit1)
        self.client.post(self.habit_url, data=habit2)
        response = self.client.get(self.base_url)
        self.assertEqual(
            response.data[0]["habit"]["name"], habit1["name"])
        self.assertEqual(
            response.data[1]["habit"]["name"], habit2["name"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_daily_week_list_view(self):
        habit1 = create_sample_habit()
        habit2 = create_sample_habit()
        self.client.post(self.habit_url, data=habit1)
        self.client.post(self.habit_url, data=habit2)
        habit1_instance = Habit.objects.get(pk=1)
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2020-01-01")
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2019-12-29")
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2020-01-04")
        response = self.client.get(f"{self.base_url}?timeframe=week")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Different date
        # Week view for 2020-01-01 is from 2019-12-29 to 2020-01-04
        response2 = self.client.get(
            f"{self.base_url}?timeframe=week&date=2020-01-01")
        self.assertEqual(len(response2.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_daily_month_list_view(self):
        habit1 = create_sample_habit()
        habit2 = create_sample_habit()
        self.client.post(self.habit_url, data=habit1)
        self.client.post(self.habit_url, data=habit2)
        habit1_instance = Habit.objects.get(pk=1)
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2020-01-01")
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2020-01-16")
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2020-01-31")
        response = self.client.get(f"{self.base_url}?timeframe=month")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Different date
        # Month view for 2020-01-01 is from 2020-01-01 to 2020-01-31
        response2 = self.client.get(
            f"{self.base_url}?timeframe=month&date=2020-01-01")
        self.assertEqual(len(response2.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_daily_year_list_view(self):
        habit1 = create_sample_habit()
        habit2 = create_sample_habit()
        self.client.post(self.habit_url, data=habit1)
        self.client.post(self.habit_url, data=habit2)
        habit1_instance = Habit.objects.get(pk=1)
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2019-01-01")
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2019-06-01")
        create_sample_daily(habit=habit1_instance,
                            user=self.user, date="2019-11-01")
        response = self.client.get(f"{self.base_url}?timeframe=year")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Different date
        # Year view for 2019-01-01 to 2019-12-31
        response2 = self.client.get(
            f"{self.base_url}?timeframe=year&date=2019-01-01")
        self.assertEqual(len(response2.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_daily_detail_edit(self):
        habit1 = create_sample_habit()
        habit2 = create_sample_habit()
        self.client.post(self.habit_url, data=habit1)
        self.client.post(self.habit_url, data=habit2)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_daily_id = response.data[0]["id"]
        # Edit finish status
        response2 = self.client.patch(
            f"{self.base_url}{first_daily_id}/", data={"finished": True})
        self.assertEqual(response2.data["finished"], True)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response3 = self.client.get(self.base_url)
        self.assertEqual(response3.data[0]["finished"], True)
        self.assertEqual(response3.data[1]["finished"], False)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        response4 = self.client.patch(
            f"{self.base_url}{first_daily_id}/", data={"finished": False})
        self.assertEqual(response4.data["finished"], False)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
