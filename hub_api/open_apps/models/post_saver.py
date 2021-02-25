from django.db import models


class Post(models.Model):
    reddit_id = models.TextField(blank=True, null=True, unique=True)
    title = models.CharField(max_length=200)
    url = models.TextField(blank=True, null=True, unique=True)
    date = models.DateField(auto_now_add=True)


class Title(models.Model):
    title = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='titles')


class SavedPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    url = models.TextField(blank=True, null=True, unique=True)
    seen = models.BooleanField(default=False)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='savedposts')
    date = models.DateField(auto_now_add=True)
