from django.db import models
from open_apps.models.apps import Apps


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    apps = models.ManyToManyField(Apps)


class UserAnalytic(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='useranalytics')
    label = models.CharField(max_length=100)
    action = models.CharField(max_length=100, default="Click")
    frequency = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=False)
    threshold = models.ForeignKey(
        'ViceThreshold', on_delete=models.CASCADE, related_name='useranalytics', blank=True, null=True)


class ViceThreshold(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='vicethreshold')
    label = models.CharField(max_length=100, unique=True)
    threshold = models.IntegerField()
