# Generated by Django 3.1.1 on 2020-12-01 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habit_tracker', '0004_habit_weekdays'),
    ]

    database_operations = [
        migrations.AlterModelTable(name="Daily", table="open_apps_daily"),
        migrations.AlterModelTable(
            name="Habit", table="open_apps_habit"),
        migrations.AlterModelTable(name="Todo", table="open_apps_todo"),
    ]

    state_operations = [
        migrations.DeleteModel(
            name='Daily',
        ),
        migrations.DeleteModel(
            name='Habit',
        ),
        migrations.DeleteModel(
            name='Todo',
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations, state_operations=state_operations)
    ]
