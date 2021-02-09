from open_apps.models.vice import ViceAnalytic


def create_vice_analytic(vice, user, obj_date):
    length = len(ViceAnalytic.objects.filter(
        user=user, date=obj_date, vice=vice))
    try:
        if length == 0:
            ViceAnalytic.objects.create(
                user=user, date=obj_date, vice=vice)
        return None
    except Exception:
        print(Exception)
        return Exception
