from datetime import date

from django.contrib.auth import get_user_model
from open_apps.utils.date_utils import get_date
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()
TEST_USERNAME = "testcase"
TEST_PASSWORD = "strong_password_123"


# Integration Tests with API
class ViceTestCase(APITestCase):
    base_url = "/api/vices/"
    sample_vice = {"name": "sample vice", "link": "https://this.link"}

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_vice_create(self):
        response = self.client.post(self.base_url, data=self.sample_vice)
        self.assertEqual(response.data["name"], self.sample_vice["name"])
        self.assertEqual(response.data["link"], self.sample_vice["link"])
        self.assertEqual(response.data["archived"], False)
        self.assertEqual(response.data["time_between"], "01:00:00")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vice_detail_update(self):
        response = self.client.post(self.base_url, data=self.sample_vice)
        response_id = response.data["id"]
        updated_vice = {"name": "updated vice"}
        response2 = self.client.patch(
            f"{self.base_url}{response_id}/", data=updated_vice)
        self.assertEqual(response2.data["name"], updated_vice["name"])
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        updated_vice2 = {"name": "updated vice 2", "time_between": "02:00:00"}
        response3 = self.client.patch(
            f"{self.base_url}{response_id}/", data=updated_vice2)
        self.assertEqual(response3.data["name"], updated_vice2["name"])
        self.assertEqual(
            response3.data["time_between"], updated_vice2["time_between"])
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_vice_detail_delete(self):
        response = self.client.post(self.base_url, data=self.sample_vice)
        response_id = response.data["id"]
        response2 = self.client.delete(f"{self.base_url}{response_id}/")
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)
        response3 = self.client.get(f"{self.base_url}{response_id}/")
        self.assertEqual(response3.data["detail"], "Not found.")

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ViceAnalyticTestCase(APITestCase):
    base_url = "/api/viceanalytics/"
    vice_url = "/api/vices/"
    sample_vice = {"name": "sample vice", "link": "https://this.link"}

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_vice_analytic_create(self):
        self.client.post(self.vice_url, data=self.sample_vice)

        response = self.client.post(self.base_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["vice"]
                         ["name"], self.sample_vice["name"])
        self.assertEqual(
            get_date({"date": response.data[0]["date"]}), date.today())
        self.assertEqual(response.data[0]["frequency"], 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(self.base_url)
        self.assertEqual(len(response2.data), 1)

    def test_vice_analytic_detail_update(self):
        self.client.post(self.vice_url, data=self.sample_vice)
        self.client.post(self.base_url)
        response = self.client.post(self.base_url)

        id_1 = response.data[0]["id"]
        response2 = self.client.patch(
            f"{self.base_url}{id_1}/", data={"hi": "there"})
        self.assertEqual(response2.data["frequency"], 1)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response3 = self.client.patch(
            f"{self.base_url}{id_1}/")
        self.assertEqual(response3.data["frequency"], 2)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
