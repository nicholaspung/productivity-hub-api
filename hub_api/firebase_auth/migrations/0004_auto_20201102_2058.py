# Generated by Django 3.1.1 on 2020-11-03 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firebase_auth', '0003_auto_20201102_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranalytic',
            name='date',
            field=models.DateField(),
        ),
    ]
