from django.db import models
from django.contrib.auth.models import User


APPS = {
    'HABIT_TRACKER': 'HABIT_TRACKER',
    'POST_SAVER': 'POST_SAVER'
}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    apps = models.TextField(default="")

    def save(self, *args, **kwargs):
        if self.apps:
            apps = self.apps.replace(' ', '').split(',')
            cleaned_apps = []
            for app in apps:
                if app in APPS:
                    cleaned_apps.append(app)
            self.apps = cleaned_apps
        super(Profile, self).save(*args, **kwargs)
