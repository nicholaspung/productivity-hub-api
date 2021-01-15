from django.contrib.auth import get_user_model
from open_apps.models.post_saver import Post, SavedPost, Title
from open_apps.serializers.post_saver_serializers import (PostSerializer,
                                                          SavedPostSerializer,
                                                          TitleSerializer)
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()
TEST_USERNAME = "testcase"
TEST_PASSWORD = "strong_password_123"


# Integration Tests with API
class PostTestCase(APITestCase):
    base_url = "/api/posts/"
    sample_post = {"title": "new todo", "url": "http://www.google.com"}

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_post_list(self):
        post1 = Post(
            title=self.sample_post['title'], url=self.sample_post['url'])
        post1.save()
        sample_post2 = {"title": 'new todo 2',
                        'url': 'http://www.duckduckgo.com'}
        post2 = Post(title=sample_post2['title'], url=sample_post2['url'])
        post2.save()

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]['title'], self.sample_post['title'])
        self.assertEqual(response.data["results"]
                         [1]['url'], sample_post2['url'])
        self.assertEqual(
            response.data["results"][0]['title'], self.sample_post['title'])
        self.assertEqual(response.data["results"]
                         [1]['url'], sample_post2['url'])

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TitleTestCase(APITestCase):
    base_url = "/api/titles/"
    sample_title = {"title": "new habit"}

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_title_create(self):
        response = self.client.post(self.base_url, data=self.sample_title)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.sample_title['title'])

    def test_title_list(self):
        self.client.post(self.base_url, data=self.sample_title)
        title2 = {'title': 'new habit 2'}
        self.client.post(self.base_url, data=title2)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.sample_title['title'])
        self.assertEqual(response.data[1]['title'], title2['title'])

    def test_title_detail_update(self):
        self.client.post(self.base_url, data=self.sample_title)

        updated_title = {"title": "updated title"}
        response = self.client.put(f"{self.base_url}{1}/", data=updated_title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_title['title'])

    def test_title_detail_delete(self):
        self.client.post(self.base_url, data=self.sample_title)
        title2 = {'title': 'new title 2'}
        self.client.post(self.base_url, data=title2)

        response = self.client.delete(f"{self.base_url}{1}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response2 = self.client.get(self.base_url)
        self.assertEqual(response2.data[0]['title'], title2['title'])
        self.assertEqual(len(response2.data), 1)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SavedPostTestCase(APITestCase):
    base_url = "/api/savedposts/"
    sample_saved_post = {"title": "new todo", "url": "http://www.google.com"}
    sample_saved_post2 = {"title": "new todo 2",
                          "url": "http://www.duckduckgo.com"}
    sample_saved_post3 = {"title": "hi there",
                          "url": "http://www.nasa.com"}
    sample_title = {"title": 'todo'}

    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME, password=TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        post1 = Post(
            title=self.sample_saved_post['title'], url=self.sample_saved_post['url'])
        post1.save()
        post2 = Post(
            title=self.sample_saved_post2['title'], url=self.sample_saved_post2['url'])
        post2.save()
        post3 = Post(
            title=self.sample_saved_post3['title'], url=self.sample_saved_post3['url'])
        post3.save()
        title1 = Title(title=self.sample_title['title'], user=self.user)
        title1.save()

    def test_saved_post_list(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'],
                         self.sample_saved_post['title'])
        self.assertEqual(response.data[1]['title'],
                         self.sample_saved_post2['title'])
        self.assertEqual(len(response.data), 2)

    def test_saved_post_detail_update(self):
        response = self.client.get(self.base_url)
        post = response.data[0]

        response2 = self.client.put(
            f"{self.base_url}{post['id']}/", data={'seen': True})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['seen'], True)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
