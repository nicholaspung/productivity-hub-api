# Generated by Django 3.1.1 on 2021-02-21 19:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('open_apps', '0010_auto_20210129_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedpost',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
