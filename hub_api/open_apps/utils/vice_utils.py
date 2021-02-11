from open_apps.models.vice import ViceAnalytic, Vice


def create_unarchived_vice_analytics(user, obj_date):
    vices = Vice.objects.filter(user=user, archived=False)
    for vice in vices:
        create_vice_analytic(vice, user, obj_date)
    return None


def create_vice_analytic(vice, user, obj_date):
    length = len(ViceAnalytic.objects.filter(
        user=user, date=obj_date, vice=vice))
    if length == 0:
        ViceAnalytic.objects.create(
            user=user, date=obj_date, vice=vice)
    return None
