# Generated by Django 3.1.1 on 2020-09-04 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]
