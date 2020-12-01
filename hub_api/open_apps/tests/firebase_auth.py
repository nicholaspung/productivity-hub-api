from datetime import date

from django.contrib.auth.models import User
from open_apps.models.firebase_auth import (APPS, Profile, UserAnalytic,
                                            ViceThreshold)
from open_apps.serializers.firebase_auth import (ProfileSerializer,
                                                 UserAnalyticSerializer,
                                                 UserSerializer)
from rest_framework import status
from rest_framework.test import APITestCase

from habit_tracker.views import get_date, week__range

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


class UserAnalyticTestCase(APITestCase):
    base_url = "/api/useranalytics/"

    def setUp(self):
        self.user = User.objects.create_user(
            username=test_username, password=test_password)
        Profile.objects.get_or_create(
            user=self.user)
        self.client.login(username=test_username, password=test_password)

    def test_user_analytic_create_post(self):
        response = self.client.post(self.base_url)
        self.assertEqual(response.data['message'], 'Analytics created.')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        analytics = UserAnalytic.objects.filter(user=self.user)
        self.assertEqual(len(analytics), 5)
        for analytic in analytics:
            self.assertEqual(analytic.frequency, 0)

        response2 = self.client.post(f"{self.base_url}?date=2020-10-09")
        self.assertEqual(response.data['message'], 'Analytics created.')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        analytics = UserAnalytic.objects.filter(
            user=self.user, date=get_date({'date': '2020-10-09'}))
        self.assertEqual(len(analytics), 5)
        for analytic in analytics:
            self.assertEqual(analytic.frequency, 0)

        label = 'Post Saver Nav'
        response3 = self.client.post(f"{self.base_url}", {'label': label})
        self.assertEqual(response3.data['message'], 'Analytics created.')
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        analytics2 = UserAnalytic.objects.filter(
            user=self.user, label=label)
        self.assertEqual(len(analytics2), 2)
        self.assertEqual(analytics2[0].frequency, 1)
        self.assertEqual(analytics2[1].frequency, 0)

        self.client.post(f"{self.base_url}?date=2020-10-10")
        self.client.post(f"{self.base_url}?date=2020-10-11")
        self.client.post(f"{self.base_url}?date=2020-10-12")
        self.client.post(f"{self.base_url}?date=2020-10-13")
        self.client.post(f"{self.base_url}?date=2020-10-14")
        self.client.post(f"{self.base_url}?date=2020-10-15")
        self.assertEqual(len(ViceThreshold.objects.filter(user=self.user)), 0)
        self.client.post(f"{self.base_url}?date=2020-10-16")
        self.assertEqual(len(ViceThreshold.objects.filter(user=self.user)), 5)
        self.client.post(f"{self.base_url}?date=2020-10-17")
        self.assertEqual(UserAnalytic.objects.filter(user=self.user,
                                                     date=get_date({'date': '2020-10-16'}))[0].threshold, None)
        self.assertEqual(UserAnalytic.objects.filter(user=self.user,
                                                     date=get_date({'date': '2020-10-17'}))[0].threshold, ViceThreshold.objects.filter(user=self.user)[0])

    def test_user_analytic_list_get(self):
        self.client.post(self.base_url)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        today = date.today()
        self.assertEqual(
            get_date({'date': response.data[0]['date']}), date.today())
        self.client.post(self.base_url)
        response2 = self.client.get(self.base_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 5)
        self.assertEqual(
            get_date({'date': response2.data[0]['date']}), date.today())
        self.assertEqual(response2.data[0]['frequency'], 0)

        self.client.post(f"{self.base_url}?date=2020-10-09")
        response3 = self.client.get(f"{self.base_url}?date=2020-10-09")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response3.data), 5)
        self.assertEqual(response3.data[0]['date'], '2020-10-09')

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
