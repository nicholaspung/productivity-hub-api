# Generated by Django 3.1.1 on 2020-09-23 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_saver', '0002_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
