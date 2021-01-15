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
    threshold = models.ForeignKey(
        'ViceThreshold', on_delete=models.CASCADE, related_name='viceanalytics', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)


class ViceThreshold(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='vicethresholds')
    name = models.CharField(max_length=100, unique=True)
    threshold = models.IntegerField(default=8)
