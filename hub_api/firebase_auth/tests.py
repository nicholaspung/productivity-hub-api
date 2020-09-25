from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import APPS, Profile
from .serializers import UserSerializer, ProfileSerializer

test_username = "testcase"
test_password = "strong_password_123"


# Integration Tests with API
class UserTestCase(APITestCase):
    base_url = "/api/user/"

    def setUp(self):
        self.user = User.objects.create_user(
            username=test_username, password=test_password)
        self.client.login(username=test_username, password=test_password)

    def test_user_list_get(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], self.user.username)

    def test_user_detail_delete(self):
        response = self.client.delete(f"{self.base_url}{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'All user data has been deleted.')
        try:
            User.objects.get(pk=self.user.id)
            self.assertEqual(True, False)
        except User.DoesNotExist:
            self.assertEqual(True, True)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileTestCase(APITestCase):
    base_url = "/api/profile/"

    def setUp(self):
        self.user = User.objects.create_user(
            username=test_username, password=test_password)
        Profile.objects.get_or_create(
            user=self.user)
        self.client.login(username=test_username, password=test_password)

    def test_profile_list_get(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_anonymous'], False)
        self.assertEqual(response.data['apps'], APPS['HABIT_TRACKER'])

    def test_profile_detail_update(self):
        response = self.client.get(self.base_url)
        apps = f"{response.data['apps']},{APPS['POST_SAVER']}"
        response2 = self.client.patch(
            f"{self.base_url}{self.user.id}/", data={'apps': apps})
        self.assertEqual(response2.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response2.data['apps'], apps)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
