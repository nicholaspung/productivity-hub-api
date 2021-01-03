from django.test import TestCase
from open_apps.utils import api_utils
from rest_framework import status


class ApiUtilTestCase(TestCase):
    def test_unused_method(self):
        response = api_utils.unused_method()
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            'not offered in this path' in response.data["message"], True)
