# Generated by Django 3.1.1 on 2020-09-23 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_saver', '0003_auto_20200923_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
