# Sample file for commands

import logging

from django.conf import settings
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


def my_job():
    #  Your job processing logic here...
    print('hello')

# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        manage_runapscheduler = BackgroundScheduler(
            timezone=settings.TIME_ZONE)
        manage_runapscheduler.add_jobstore(DjangoJobStore(), "default")

        manage_runapscheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
        print(dir(manage_runapscheduler))
        print(manage_runapscheduler.print_jobs())
        # manage_runapscheduler.add_job(
        #     delete_old_job_executions,
        #     trigger=CronTrigger(
        #         day_of_week="mon", hour="00", minute="00"
        #     ),  # Midnight on Monday, before start of the next work week.
        #     id="delete_old_job_executions",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info(
        #     "Added weekly job: 'delete_old_job_executions'."
        # )

        try:
            logger.info("Starting manage_runapscheduler...")
            manage_runapscheduler.start()
            while True:
                time.sleep(4)
        except KeyboardInterrupt:
            print('Error')
            logger.info("Stopping manage_runapscheduler...")
            manage_runapscheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
