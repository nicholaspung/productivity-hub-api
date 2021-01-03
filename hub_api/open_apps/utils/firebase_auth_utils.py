from firebase_admin import auth
from open_apps.models.firebase_auth import UserAnalytic, ViceThreshold
from open_apps.utils.date_utils import get_date
from rest_framework import status
from rest_framework.response import Response


def delete_firebase_user(user):
    firebase_uid = user.username
    try:
        firebase_user = auth.get_user(firebase_uid)
        if firebase_user:
            auth.delete_user(firebase_user.uid)
    except auth.UserNotFoundError as err:
        return Response({'error': err.default_message},
                        status=status.HTTP_404_NOT_FOUND)


def increment_user_analytic_frequency(request):
    obj_date = get_date(request.query_params)  # 2020-10-10
    label_request = request.data.get('label', None)
    if label_request:
        obj, created = UserAnalytic.objects.get_or_create(
            user=request.user, label=label_request, date=obj_date)
        if not created:
            obj.frequency += 1
            obj.save()
            return True
    return False


def create_vice_threshold(user, label):
    filtered_ua = UserAnalytic.objects.filter(user=user, label=label)
    num_of_ua_for_label = len(filtered_ua)
    if num_of_ua_for_label > 7:
        avg_frequency_of_ua = sum(
            [analytic.frequency for analytic in filtered_ua]) // num_of_ua_for_label
        if avg_frequency_of_ua < 5:
            avg_frequency_of_ua = 5
        vice_threshold, _ = ViceThreshold.objects.get_or_create(
            user=user, label=label, threshold=avg_frequency_of_ua)
        return vice_threshold
    return None


def create_user_analytic(user, label, obj_date, threshold):
    length = len(UserAnalytic.objects.filter(
        user=user, label=label, date=obj_date))
    if length == 0:
        UserAnalytic.objects.create(
            user=user, label=label, date=obj_date, threshold=threshold)
