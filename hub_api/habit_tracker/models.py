import datetime

import pytz
from django.db import models

ENUM_PRIORITY_CHOICES = (
    ("none", "NONE"),
    ("high", "HIGH"),
    ("low", "LOW")
)


class Todo(models.Model):
    name = models.CharField(max_length=280)
    description = models.TextField(blank=True, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    finished = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=4, choices=ENUM_PRIORITY_CHOICES, default=ENUM_PRIORITY_CHOICES[0])
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
        super(Todo, self).save(*args, **kwargs)


class Habit(models.Model):
    def grabLastNumberInUnfinishedHabits():
        return Habit.objects.filter(user='auth.User').count()

    name = models.CharField(max_length=280)
    description = models.TextField(blank=True, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=1)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='habits')
    archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_order = Habit.objects.filter(user=self.user).count()
            if last_order is not None:
                self.order = last_order
        super(Habit, self).save(*args, **kwargs)


class Daily(models.Model):
    date = models.DateField(auto_now_add=True)
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name='dailies')
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='dailies')
