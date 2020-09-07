# Generated by Django 3.1.1 on 2020-09-07 03:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=280)),
                ('description', models.TextField(blank=True, default='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_finished', models.DateTimeField(blank=True, null=True)),
                ('finished', models.BooleanField(default=False)),
                ('priority', models.CharField(choices=[('NONE', 'none'), ('HIGH', 'high'), ('LOW', 'low')], default=('NONE', 'none'), max_length=4)),
                ('order', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=280)),
                ('description', models.TextField(blank=True, default='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(default=1)),
                ('archived', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('finished', models.BooleanField(default=False)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailies', to='habit_tracker.habit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
