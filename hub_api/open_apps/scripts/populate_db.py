from open_apps.models.app import APPS, App


def populate_apps(text=True):
    app_text = ["The following apps have been populated:"]
    for app_title in APPS:
        _, created = App.objects.get_or_create(title=app_title)
        if created:
            app_text.append(f"    {app_title}")

    if text is False:
        return

    if len(app_text) > 1:
        for text in app_text:
            print(text)
    else:
        print("No additional apps have been added.")
