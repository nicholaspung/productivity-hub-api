from django.db import models


class Apps(models.Model):
    title = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['title']
