from open_apps.models.vice import Vice, ViceAnalytic, ViceThreshold


def create_vice_analytic(vice, user, obj_date):
    try:
        name_of_vice = vice.name
        vice_thresholds = ViceThreshold.objects.filter(
            user=user, name=name_of_vice)
        if len(vice_thresholds) > 0:
            threshold = vice_thresholds[0]
        else:
            threshold = None

        vice_analytic_for_day = ViceAnalytic.objects.filter(
            user=user, date=obj_date, vice=vice)
        if len(vice_analytic_for_day) < 1:
            ViceAnalytic.objects.create(
                user=user, threshold=threshold, date=obj_date, vice=vice)
        return None
    except Exception:
        print(Exception)
        return Exception


def attach_vice_threshold_to_analytic(user, name, id):
    vice = Vice.objects.get(user=user, name=name)
    v_a_objs = ViceAnalytic.objects.filter(
        vice=vice, user=user).order_by('-date')
    v_a = v_a_objs[0]  # Latest user analytic
    new_v_t = ViceThreshold.objects.get(pk=id)
    v_a.threshold = new_v_t
    v_a.save()
