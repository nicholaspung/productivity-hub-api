from datetime import date
from django.contrib.auth import get_user_model

from django.test import TestCase
from open_apps.utils import firebase_auth_utils
from open_apps.models.firebase_auth import LABELS
from open_apps.models.firebase_auth import UserAnalytic

User = get_user_model()
TEST_USERNAME = "testcase"
TEST_PASSWORD = "strong_password_123"


class FakeClass():
    hi = 'hi'


class FirebaseAuthUtilTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_delete_firebase_user(self):
        pass

    def test_increment_user_analytic_frequency(self):
        request = FakeClass()
        setattr(request, 'query_params', {'date': '2020-10-10'})
        setattr(request, 'data', {'label': LABELS[0]})
        setattr(request, 'user', self.user)
        response = firebase_auth_utils.increment_user_analytic_frequency(
            request)
        self.assertEqual(response, False)

        response2 = firebase_auth_utils.increment_user_analytic_frequency(
            request)
        self.assertEqual(response2, True)

    def test_create_user_analytic_threshold(self):
        label = LABELS[0]
        response = firebase_auth_utils.create_user_analytic_threshold(
            self.user, label)
        self.assertEqual(response, None)

        firebase_auth_utils.create_user_analytic(
            self.user, label, date(2020, 1, 1), None)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date(2020, 1, 2), None)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date(2020, 1, 3), None)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date(2020, 1, 4), None)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date(2020, 1, 5), None)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date(2020, 1, 6), None)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date(2020, 1, 7), None)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date(2020, 1, 8), None)

        response2 = firebase_auth_utils.create_user_analytic_threshold(
            self.user, label)
        self.assertEqual(response2.threshold, 5)
        self.assertEqual(response2.label, label)

    def test_create_user_analytic(self):
        label = LABELS[0]
        date1 = date(2020, 10, 10)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date1, None)
        self.assertEqual(
            len(UserAnalytic.objects.filter(user=self.user)), 1)
        self.assertEqual(UserAnalytic.objects.filter(
            user=self.user, date=date1)[0].date, date1)

        date2 = date(2020, 12, 12)
        firebase_auth_utils.create_user_analytic(
            self.user, label, date2, None)
        self.assertEqual(
            len(UserAnalytic.objects.filter(user=self.user)), 2)
        self.assertEqual(UserAnalytic.objects.filter(
            user=self.user, date=date2)[0].date, date2)
