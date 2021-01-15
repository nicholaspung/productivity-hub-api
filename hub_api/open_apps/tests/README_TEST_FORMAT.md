# How to format tests

Example API test case:

```
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()
TEST_USERNAME = "testcase"
TEST_PASSWORD = "strong_password_123"


class *Sample*TestCase(APITestCase):
    base_url = 'any_url_that_needs_to_be_tested'
    sample_*sample* = {'sample': 'object that is needed for test'}

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_*sample*_list(self):
        pass

    # If view hijacks list view to show a profile detail
    def test_*sample*_list_detail(self):
        pass

    def test_*sample*_create(self):
        pass

    def test_*sample*_detail_retrive(self):
        pass

    def test_*sample*_detail_update(self):
        pass

    def test_*sample*_detail_delete(self):
        pass

    # If view has permissions, this is a sample test
    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

```

Example utility test case:

```
from django.test import TestCase


class SampleTestCase(TestCase):
    '''
    Methods to be tested
    Utils can generally different and until there seems to be a common theme between utils, there is no real convention.
    '''
```
