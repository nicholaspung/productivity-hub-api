# Generated by Django 3.1.1 on 2020-09-24 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_saver', '0004_auto_20200923_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedpost',
            name='url',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]