from open_apps.models.app import APPS, App


def populate_apps():
    for app_title in APPS:
        App.objects.get_or_create(title=app_title)
