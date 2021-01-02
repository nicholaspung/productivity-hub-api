from datetime import date

from django.contrib.auth import get_user_model
from open_apps.models.app import DEFAULT_APPS, App
from open_apps.models.firebase_auth import (LABELS, Profile, UserAnalytic,
                                            ViceThreshold)
from open_apps.scripts.populate_db import populate_apps
from open_apps.utils.date_utils import get_date
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()
TEST_USERNAME = "testcase"
TEST_PASSWORD = "strong_password_123"


# Integration Tests with API
class UserTestCase(APITestCase):
    base_url = "/api/user/"

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_user_detail_delete(self):
        response = self.client.delete(f"{self.base_url}{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        try:
            User.objects.get(pk=self.user.id)
            self.assertEqual(True, False)
        except User.DoesNotExist:
            self.assertEqual(True, True)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(f"{self.base_url}{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileTestCase(APITestCase):
    base_url = "/api/profile/"

    def setUp(self):
        populate_apps()
        app = App.objects.all()[0]
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        Profile.objects.get_or_create(user=self.user)
        self.user.profile.apps.add(app)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_profile_detail_list(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        apps = [app.id for app in App.objects.filter(title=DEFAULT_APPS[0])]
        self.assertEqual(response.data['apps'], apps)

    def test_profile_detail_update(self):
        apps = [app.id for app in App.objects.all()[:3]]
        response = self.client.patch(
            f"{self.base_url}{self.user.id}/", data={"apps": apps})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['apps'], apps)

        apps2 = [app.id for app in App.objects.all()[:1]]
        response2 = self.client.patch(
            f"{self.base_url}{self.user.id}/", data={"apps": apps2})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['apps'], apps2)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAnalyticTestCase(APITestCase):
    base_url = "/api/useranalytics/"

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        Profile.objects.get_or_create(
            user=self.user)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_user_analytic_create_post(self):
        response = self.client.post(self.base_url)
        self.assertEqual(response.data['message'], 'Analytics created.')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        analytics = UserAnalytic.objects.filter(user=self.user)
        self.assertEqual(len(analytics), 5)
        for analytic in analytics:
            self.assertEqual(analytic.frequency, 0)

        date_param = '2020-10-09'
        response2 = self.client.post(f"{self.base_url}?date={date_param}")
        self.assertEqual(response2.data['message'], 'Analytics created.')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        analytics = UserAnalytic.objects.filter(
            user=self.user, date=get_date({'date': date_param}))
        self.assertEqual(len(analytics), 5)
        for analytic in analytics:
            self.assertEqual(analytic.frequency, 0)

        label = 'Post Saver Nav'
        response3 = self.client.post(f"{self.base_url}", {'label': label})
        self.assertEqual(response3.data['message'], 'Analytics incremented.')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
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
                                                     date=get_date({'date': '2020-10-15'}))[0].threshold, None)
        self.assertEqual(UserAnalytic.objects.filter(user=self.user,
                                                     date=get_date({'date': '2020-10-17'}))[0].threshold, ViceThreshold.objects.filter(user=self.user)[0])

    def test_user_analytic_list_get(self):
        self.client.post(self.base_url)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        today = date.today()
        self.assertEqual(
            get_date({'date': response.data[0]['date']}), today)
        self.client.post(self.base_url)
        response2 = self.client.get(self.base_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 5)
        self.assertEqual(
            get_date({'date': response2.data[0]['date']}), today)
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


class ViceThresholdTestCase(APITestCase):
    base_url = "/api/vicethreshold/"
    user_analytic_url = '/api/useranalytics/'

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        Profile.objects.get_or_create(
            user=self.user)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_vice_threshold_list_create(self):
        response = self.client.post(
            self.base_url, data={'label': LABELS[0], 'threshold': 1})
        self.assertEqual('Unable to attach' in response.data["message"], True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response2 = self.client.post(
            self.base_url, data={'label': 'Fake label', 'threshold': 1})
        self.assertEqual('Label not found' in response2.data["message"], True)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.post(self.user_analytic_url)
        response3 = self.client.post(
            self.base_url, data={'label': LABELS[0], 'threshold': 1})
        self.assertEqual(
            'Label Already Exists' in response3.data['label'][0].title(), True)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

        response4 = self.client.post(
            self.base_url, data={'label': LABELS[1], 'threshold': 1})
        self.assertEqual(response4.data['label'], LABELS[1])
        self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response4.data['id'], UserAnalytic.objects.filter(
            label=LABELS[1])[0].threshold.id)

    def test_vice_threshold_detail_update(self):
        response = self.client.post(
            self.base_url, data={'label': LABELS[1], 'threshold': 1})
        threshold = 5
        response1 = self.client.patch(
            f"{self.base_url}{response.data['id']}/", {'threshold': threshold})
        self.assertEqual(response1.data['threshold'], threshold)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
