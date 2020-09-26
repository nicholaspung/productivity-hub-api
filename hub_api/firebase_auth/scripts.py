from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore, register_job
from django_apscheduler.models import DjangoJobExecution
from firebase_admin import auth

from .models import Profile

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, 'interval', weeks=1, replace_existing=True)
def prune_anonymous_users_in_firebase_and_django():
    """
    This job deletes all anonymous users that haven't used their account in a week from both Firebase and Django
    """
    page = auth.list_users()
    anonymous_users = []
    for user in page.users:
        user_last_refresh = date.fromtimestamp(
            user.user_metadata.last_refresh_timestamp / 1e3)
        logged_within_one_week = date.today() - timedelta(days=7) > user_last_refresh
        if user.email is None and logged_within_one_week:
            anonymous_users.append(user.uid)
    result = auth.delete_users(anonymous_users)

    if len(result.errors) == 0:
        profiles = Profile.objects.filter(is_anonymous=True)
        for profile in profiles:
            profile.user.delete()

    print('Successfully deleted {0} users'.format(result.success_count))
    print('Failed to delete {0} users'.format(result.failure_count))
    for err in result.errors:
        print('error #{0}, reason: {1}'.format(result.index, result.reason))

# Executes when server starts
# prune_anonymous_users_in_firebase_and_django()


@register_job(scheduler, 'interval', weeks=1, replace_existing=True)
def delete_old_job_executions():
    """
    This job deletes all apscheduler job executions older than `max_age` from the database.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age=604_800)
