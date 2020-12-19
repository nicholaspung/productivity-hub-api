from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from open_apps.scripts.firebase_auth_scripts import (
    delete_old_job_executions, prune_anonymous_users_in_firebase_and_django)

job_defaults = {
    'max_instances': 1,
    'replace_existing': True
}
scheduler = BackgroundScheduler(
    timezone=settings.TIME_ZONE, job_defaults=job_defaults)
scheduler.add_jobstore(DjangoJobStore(), "default")


@scheduler.scheduled_job('interval', id='firebase_auth.scripts.prune_anonymous_users_in_firebase_and_django', weeks=1)
def dev_prune_anonymous_users_in_firebase_and_django():
    prune_anonymous_users_in_firebase_and_django()


@scheduler.scheduled_job('interval', id='firebase_auth.scripts.delete_old_job_executions', weeks=1)
def dev_delete_old_job_executions():
    delete_old_job_executions()


# Executes when server starts
# prune_anonymous_users_in_firebase_and_django()
# delete_old_job_executions()
