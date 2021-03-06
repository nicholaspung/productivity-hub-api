# Generated by Django 3.1.1 on 2020-12-01 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firebase_auth', '0006_auto_20201107_2110'),
    ]

    database_operations = [
        migrations.AlterModelTable(name="Profile", table="open_apps_profile"),
        migrations.AlterModelTable(
            name="UserAnalytic", table="open_apps_useranalytic"),
        migrations.AlterModelTable(
            name="ViceThreshold", table="open_apps_vicethreshold"),
    ]

    state_operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='UserAnalytic',
        ),
        migrations.DeleteModel(
            name='ViceThreshold',
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations, state_operations=state_operations)
    ]
