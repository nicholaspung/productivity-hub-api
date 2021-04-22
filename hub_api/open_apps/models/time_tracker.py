from datetime import time
from django.db import models


class TrackTimeName(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="tracktimename")
    name = models.CharField(max_length=200)
    archived = models.BooleanField(default=False)


class TrackTime(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="tracktime")
    date = models.DateField(auto_now_add=False)
    track_time_name = models.ForeignKey(
        TrackTimeName, on_delete=models.CASCADE, related_name='tracktime')
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=True, null=True)
    total_time = models.IntegerField(blank=True, null=True)  # saved in seconds

    def save(self, *args, **kwargs):
        if self.end_time:
            total_seconds = self.end_time - self.start_time
            rounded_total_seconds = round(total_seconds.total_seconds())
            self.total_time = rounded_total_seconds
        super(TrackTime, self).save(*args, **kwargs)


class TimeTrackerPreferences(models.Model):
    profile = models.OneToOneField(
        'open_apps.Profile', on_delete=models.CASCADE)
    enable_pomodoro = models.BooleanField(default=True)
    pomodoro_interval_time = models.TimeField(
        auto_now=False, auto_now_add=False, default=time(minute=25))
    break_interval_time = models.TimeField(
        auto_now=False, auto_now_add=False, default=time(minute=5))
