# Generated by Django 3.1.1 on 2021-05-11 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_apps', '0012_timetrackerpreferences_tracktime_tracktimename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracktime',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
