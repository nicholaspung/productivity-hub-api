# Generated by Django 3.1.1 on 2020-09-23 21:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_saver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.date(2020, 9, 23)),
        ),
    ]
