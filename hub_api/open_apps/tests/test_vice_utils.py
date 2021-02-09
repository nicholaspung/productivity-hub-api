from django.test import TestCase
from open_apps.utils import vice_utils
from django.contrib.auth import get_user_model
from open_apps.models.vice import Vice, ViceAnalytic
from datetime import date

User = get_user_model()
TEST_USERNAME = "testcase"
TEST_PASSWORD = "strong_password_123"


class SampleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_create_vice_analytic(self):
        vice1 = Vice(name="hi", link="hi link", user=self.user)
        vice1.save()
        vice2 = Vice(name="bye", link="bye link", user=self.user)
        vice2.save()
        today = date.today()

        vice_utils.create_vice_analytic(vice1, self.user, today)
        viceAnalytic1 = ViceAnalytic.objects.filter(vice=vice1)
        self.assertEqual(len(viceAnalytic1), 1)
        vice_utils.create_vice_analytic(vice1, self.user, today)
        viceAnalytic1v2 = ViceAnalytic.objects.filter(vice=vice1)
        self.assertEqual(len(viceAnalytic1v2), 1)

        vice_utils.create_vice_analytic(vice2, self.user, today)
        viceAnalytic2 = ViceAnalytic.objects.filter(vice=vice2)
        self.assertEqual(len(viceAnalytic2), 1)
        vice_utils.create_vice_analytic(vice2, self.user, today)
        viceAnalytic2v2 = ViceAnalytic.objects.filter(vice=vice2)
        self.assertEqual(len(viceAnalytic2v2), 1)
