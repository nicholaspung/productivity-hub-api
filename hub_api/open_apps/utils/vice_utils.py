from open_apps.models.vice import ViceAnalytic


def create_vice_analytic(vice, user, obj_date):
    try:
        vice_analytic_for_day = ViceAnalytic.objects.filter(
            user=user, date=obj_date, vice=vice)
        if len(vice_analytic_for_day) < 1:
            ViceAnalytic.objects.create(
                user=user, date=obj_date, vice=vice)
        return None
    except Exception:
        print(Exception)
        return Exception
