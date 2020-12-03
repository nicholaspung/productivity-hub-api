from open_apps.models.apps import Apps


def populate_apps():
    apps = ['Habit Tracker, Post Saver']

    for app_title in apps:
        Apps.objects.create(title=app_title)
