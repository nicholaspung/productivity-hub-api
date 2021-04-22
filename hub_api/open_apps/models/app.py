from django.db import models


APPS = ['Habit Tracker', 'Post Saver', 'Vices', 'Time Tracker']
DEFAULT_APPS = [APPS[0], APPS[3]]


class App(models.Model):
    title = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['title']
