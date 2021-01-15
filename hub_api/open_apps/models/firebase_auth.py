from django.db import models


LABELS = ["Post Saver Nav", "Saved Post Title",
          "Saved Post Refresh", "All Post Title", "All Post Refresh"]


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    apps = models.ManyToManyField('App', related_name="profile")
    email = models.CharField(max_length=100, blank=True, null=True)


class UserAnalytic(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='useranalytics')
    label = models.CharField(max_length=100)
    action = models.CharField(max_length=100, default="Click")
    frequency = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=False)
    threshold = models.ForeignKey(
        'UserAnalyticThreshold', on_delete=models.CASCADE, related_name='useranalytics', blank=True, null=True)


class UserAnalyticThreshold(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='useranalyticthresholds')
    label = models.CharField(max_length=100, unique=True)
    threshold = models.IntegerField(default=0)
