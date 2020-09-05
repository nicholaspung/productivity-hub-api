# Generated by Django 3.1.1 on 2020-09-05 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('habit_tracker', '0002_auto_20200905_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='habit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailies', to='habit_tracker.habit'),
        ),
        migrations.AlterField(
            model_name='daily',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='habit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='todo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to=settings.AUTH_USER_MODEL),
        ),
    ]