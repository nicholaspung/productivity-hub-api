from django.db import models


APPS = ['Habit Tracker', 'Post Saver', 'Vices']
DEFAULT_APPS = [APPS[0]]


class App(models.Model):
    title = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['title']
