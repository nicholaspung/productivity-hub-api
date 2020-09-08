import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Daily, Habit, Todo
from .serializers import (DailySerializer, HabitSerializer, TodoSerializer,
                          UserSerializer)

test_username = "testcase"
test_password = "strong_password_123"

# Integration Tests with API


class TodoTestCase(APITestCase):
    list_url = "/habits/"

    def setUp(self):
        self.user = User.objects.create_user(
            username=test_username, password=test_password)
        self.client.login(username=test_username, password=test_password)

    def test_todo_create_view(self):
        todo = {"name": "new todo", "description": "new description"}
        response = self.client.post(self.list_url, data=todo)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], todo['name'])
        self.assertEqual(response.data['description'], todo['description'])

    def test_todo_list_view(self):
        todo = {"name": "new todo", "description": "new description"}
        self.client.post(self.list_url, data=todo)
        todo2 = {"name": "new todo 2", "description": "new description 2"}
        self.client.post(self.list_url, data=todo2)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], todo['name'])
        self.assertEqual(response.data[1]['name'], todo2['name'])
        self.assertEqual(response.data[0]['description'], todo['description'])
        self.assertEqual(response.data[1]['description'], todo2['description'])

    def test_todo_detail_delete(self):
        pass

    def test_todo_detail_edit(self):
        # Edit name, description
        # Edit finish status
        # Edit priority
        pass

    def test_todo_detail_order_switch(self):
        pass

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)

        pass


'''
class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = new_user
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_habit_list_view(self):
        pass

    def test_habit_detail_delete(self):
        pass

    def test_habit_detail_edit(self):
        # Edit name, description
        # Edit archive status
        pass

    def test_habit_detail_order_switch(self):
        pass

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)

        pass


class DailyTestCase(APITestCase):
    def setUp(self):
        self.user = new_user
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_daily_list_view(self):
        pass

    def test_daily_week_list_view(self):
        pass

    def test_daily_month_list_view(self):
        pass

    def test_daily_year_list_view(self):
        pass

    def test_daily_detail_edit(self):
        # Edit finish status
        pass

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)

        pass
'''

'''
class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"username": "testcase", "email": "test@localhost.app",
                "password1": "some_strong_psw", "password2": "some_strong_psw"}
        response = self.client.post("/api/rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):
    list_url = reverse("profile-list")

    def setUp(self):
        self.user = User.objects.create_user(
            username="davinci", password="some_strong_psw")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse("profile-detail"), kwargs={"pk": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "davinci")

    def test_profile_update_by_owner(self):
        response = self.client.put(reverse("profile-detail"), kwargs={"pk": 1}, {"city": "Anchiano", "bio": "Renaissance Genius"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
                         "id": 1, "user": "davinci", "bio": "Renaissance Genius", "city": "Anchiano", "avatar": None})

    def test_profile_update_by_random_user(self):
        random_user = User.objects.create_user(
            username="random", password="strong_password_123")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("profile-detail"), kwargs={"pk": 1}, {"city": "Hacked!!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
'''
