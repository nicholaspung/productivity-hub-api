from datetime import time

from django.db import models


class Vice(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="vices")
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    archived = models.BooleanField(default=False)


class ViceAnalytic(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="viceanalytics")
    frequency = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=False)
    vice = models.ForeignKey(
        'Vice', on_delete=models.CASCADE, related_name='viceanalytics')
    last_updated = models.DateTimeField(auto_now=True)
    time_between = models.TimeField(
        auto_now=False, auto_now_add=False, default=time(hour=1))
