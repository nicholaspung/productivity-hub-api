from open_apps.models.vice import ViceAnalytic


def create_vice_analytic(vice, user, obj_date):
    try:
        ViceAnalytic.objects.get_or_create(
            user=user, date=obj_date, vice=vice)
        return None
    except Exception:
        print(Exception)
        return Exception
