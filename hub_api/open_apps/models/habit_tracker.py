import datetime

import pytz
from django.db import models

ENUM_PRIORITY_CHOICES = ['NONE', 'HIGH', 'LOW']


class Todo(models.Model):
    name = models.CharField(max_length=280)
    description = models.TextField(blank=True, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    finished = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=4, default=ENUM_PRIORITY_CHOICES[0])
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='todos')
    order = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_order = Todo.objects.filter(user=self.user).count()
            if last_order is not None:
                self.order = last_order
        if self.finished == True:
            self.date_finished = datetime.datetime.now(tz=pytz.UTC)
        else:
            self.date_finished = None
        if self.priority not in ENUM_PRIORITY_CHOICES:
            self.priority = ENUM_PRIORITY_CHOICES[0]
        super(Todo, self).save(*args, **kwargs)


class Habit(models.Model):
    name = models.CharField(max_length=280)
    description = models.TextField(blank=True, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=1)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='habits')
    archived = models.BooleanField(default=False)
    weekdays = models.TextField(default="Sun,Mon,Tue,Wed,Thu,Fri,Sat")

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_order = Habit.objects.filter(user=self.user).count()
            if last_order is not None:
                self.order = last_order
        super(Habit, self).save(*args, **kwargs)


class Daily(models.Model):
    date = models.DateField(auto_now_add=False)
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name='dailies')
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='dailies')
