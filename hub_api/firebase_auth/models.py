from django.contrib.auth.models import User
from django.db import models

APPS = {
    'HABIT_TRACKER': 'HABIT_TRACKER',
    'POST_SAVER': 'POST_SAVER'
}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    apps = models.TextField(default="")

    def save(self, *args, **kwargs):
        if self._state.adding:
            default_app = APPS["HABIT_TRACKER"]
            self.apps = f"{default_app}"
        elif self.apps:
            apps = self.apps.replace(' ', '').split(',')
            cleaned_apps = []
            for app in apps:
                if app in APPS:
                    cleaned_apps.append(app)
            self.apps = ','.join(cleaned_apps)
        super(Profile, self).save(*args, **kwargs)


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
