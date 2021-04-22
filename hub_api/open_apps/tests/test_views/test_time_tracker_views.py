from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from datetime import datetime, timedelta
from open_apps.models.firebase_auth import Profile
from open_apps.scripts.populate_db import populate_apps
from open_apps.models.app import DEFAULT_APPS, App

User = get_user_model()
TEST_USERNAME = "testcase"
TEST_PASSWORD = "strong_password_123"


class TrackTimeNameTestCase(APITestCase):
    base_url = '/api/tracktimename/'
    sample_track_time_name = {'name': 'samepl time tracker name'}

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_track_time_name_create(self):
        response = self.client.post(
            self.base_url, data=self.sample_track_time_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],
                         self.sample_track_time_name['name'])
        self.assertEqual(response.data['archived'], False)

    def test_track_time_name_list(self):
        self.client.post(self.base_url, data=self.sample_track_time_name)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'],
                         self.sample_track_time_name['name'])

        # Archived Time Tracker Names
        archived_track_time_name = {'name': 'archive', 'archived': True}
        self.client.post(self.base_url, data=archived_track_time_name)
        response2 = self.client.get(f"{self.base_url}?archived=True")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(response2.data[0]['archived'], True)

    def test_track_time_name_detail_update(self):
        response = self.client.post(
            self.base_url, data=self.sample_track_time_name)
        obj_id = response.data['id']
        new_name = {'name': 'new name', 'archived': True}
        response2 = self.client.put(f"{self.base_url}{obj_id}/", data=new_name)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['name'], new_name['name'])
        self.assertEqual(response2.data['archived'], new_name['archived'])

    def test_track_time_name_detail_delete(self):
        response = self.client.post(
            self.base_url, data=self.sample_track_time_name)
        obj_id = response.data['id']
        response2 = self.client.get(self.base_url)
        self.assertEqual(len(response2.data), 1)
        self.client.delete(f"{self.base_url}{obj_id}/")
        response3 = self.client.get(self.base_url)
        self.assertEqual(len(response3.data), 0)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TrackTimeTestCase(APITestCase):
    base_url = '/api/tracktime/'
    track_time_name_url = '/api/tracktimename/'
    sample_track_time_name = {'name': 'sample track name'}

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def util_create_track_time_items(self, obj_data=None, obj_date="2021-04-04"):
        new_obj_data = obj_data or self.sample_track_time_name
        response = self.client.post(
            self.track_time_name_url, data=new_obj_data)
        obj_id = response.data['id']

        track_time_name = {'date': obj_date,
                           'track_time_name': obj_id, 'start_time': datetime.now()}
        response2 = self.client.post(
            self.base_url, data=track_time_name)

        return [response2, track_time_name]

    def test_track_time_create(self):
        [response, track_time_name] = self.util_create_track_time_items()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['date'],
                         track_time_name['date'])
        self.assertEqual(
            response.data['track_time_name']['id'], track_time_name['track_time_name'])
        self.assertEqual(
            response.data['start_time'], f"{track_time_name['start_time'].isoformat()}Z")

    def test_track_time_list(self):
        today = datetime.now().date().isoformat()
        [response, _] = self.util_create_track_time_items(
            obj_date=today)
        self.util_create_track_time_items()
        response2 = self.client.get(self.base_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(response2.data[0]['track_time_name'],
                         response.data['track_time_name'])

    def test_track_time_detail_update(self):
        # Can only update for the day of tracked times
        today = datetime.now().date().isoformat()
        [response, _] = self.util_create_track_time_items(obj_date=today)
        obj_id = response.data['id']
        end_time = datetime.now(
        ) + timedelta(minutes=25)
        new_data = {'end_time': end_time,
                    'start_time': response.data['start_time'], 'date': response.data['date'], 'track_time_name': obj_id}
        response2 = self.client.put(
            f"{self.base_url}{obj_id}/", data=new_data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['end_time'],
                         f"{new_data['end_time'].isoformat()}Z")
        self.assertEqual(response2.data['total_time'] is not None, True)

        # Change track_time_name
        new_track_time_name = {'name': 'new name'}
        response3 = self.client.post(
            self.track_time_name_url, data=new_track_time_name)
        change_track_time_name = new_data.copy()
        change_track_time_name['track_time_name'] = response3.data['id']
        response4 = self.client.put(
            f"{self.base_url}{obj_id}/", data=change_track_time_name)
        self.assertEqual(
            response4.data['track_time_name']['name'], response3.data['name'])
        self.assertEqual(
            response4.data['start_time'], response2.data['start_time'])
        self.assertEqual(response4.data['end_time'],
                         response2.data['end_time'])
        self.assertEqual(
            response4.data['total_time'], response2.data['total_time'])

    def test_track_time_detail_delete(self):
        today = datetime.now().date().isoformat()
        self.util_create_track_time_items(obj_date=today)
        response = self.client.get(self.base_url)
        self.assertEqual(len(response.data), 1)
        obj_id = response.data[0]['id']
        self.client.delete(f"{self.base_url}{obj_id}/")
        response3 = self.client.get(self.base_url)
        self.assertEqual(len(response3.data), 0)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TimeTrackerPreferencesTestCase(APITestCase):
    base_url = "/api/tracktimepreferences/"
    profile_url = "/api/profile/"
    empty_time_tracker_preferences = {
        "enable_pomodoro": True, 'pomodoro_interval_time': '00:25:00', 'break_interval_time': '00:05:00'}

    def setUp(self):
        populate_apps(text=False)
        app = App.objects.all()[0]
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        Profile.objects.get_or_create(user=self.user)
        self.user.profile.apps.add(app)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_profile_detail_update(self):
        # Make sure account has time tracker app
        test_apps = App.objects.all()[:3]
        apps_id = [app.id for app in test_apps]
        response = self.client.patch(
            f"{self.profile_url}{self.user.id}/", data={"apps": apps_id})
        response_time_tracker = response.data['app_preferences']['time_tracker']
        response_time_tracker_id = response_time_tracker['id']
        self.assertEqual(response_time_tracker['enable_pomodoro'],
                         self.empty_time_tracker_preferences['enable_pomodoro'])
        self.assertEqual(response_time_tracker['pomodoro_interval_time'],
                         self.empty_time_tracker_preferences['pomodoro_interval_time'])
        self.assertEqual(response_time_tracker['break_interval_time'],
                         self.empty_time_tracker_preferences['break_interval_time'])

        # Test update
        new_preferences = {'enable_pomodoro': True,
                           'pomodoro_interval_time': '00:30:00', 'break_interval_time': '00:30:00'}
        response2 = self.client.patch(
            f"{self.base_url}{response_time_tracker_id}/", data=new_preferences)
        self.assertEqual(
            response2.data['enable_pomodoro'], new_preferences['enable_pomodoro'])
        self.assertEqual(
            response2.data['pomodoro_interval_time'], new_preferences['pomodoro_interval_time'])
        self.assertEqual(
            response2.data['break_interval_time'], new_preferences['break_interval_time'])

        result = self.client.get(self.profile_url)
        time_tracker_result = result.data['app_preferences']['time_tracker']
        self.assertEqual(
            time_tracker_result['enable_pomodoro'], new_preferences['enable_pomodoro'])
        self.assertEqual(
            time_tracker_result['pomodoro_interval_time'], new_preferences['pomodoro_interval_time'])
        self.assertEqual(
            time_tracker_result['break_interval_time'], new_preferences['break_interval_time'])

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f"{self.base_url}{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
