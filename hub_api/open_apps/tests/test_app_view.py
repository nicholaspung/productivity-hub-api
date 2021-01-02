from open_apps.models.app import App
from open_apps.scripts.populate_db import populate_apps
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class AppTestCase(APITestCase):
    base_url = reverse('apps')

    def setUp(self):
        populate_apps()

    def test_app_detail_list(self):
        apps = App.objects.all()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_apps = [{'id': app.id, 'title': app.title} for app in apps]
        self.assertEqual(response.data, serialized_apps)
