from datetime import date, datetime, timedelta

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from post_saver.scripts import subreddit_scraper, genkan_website_scraper, delete_old_posts, delete_old_seen_saved_posts
from firebase_auth.scripts import prune_anonymous_users_in_firebase_and_django, delete_old_job_executions


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(
            timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # firebase auth scripts
        scheduler.add_job(prune_anonymous_users_in_firebase_and_django, trigger=CronTrigger(day_of_week=0, hour="00", minute="00"),
                          id="firebase_auth.scripts.prune_anonymous_users_in_firebase_and_django", replace_existing=True, max_instances=1)
        scheduler.add_job(delete_old_job_executions, trigger=CronTrigger(day_of_week=0, hour="00", minute="00"),
                          id="firebase_auth.scripts.delete_old_job_executions", replace_existing=True, max_instances=1)

        # post saver scripts
        scheduler.add_job(subreddit_scraper, trigger=CronTrigger(minute="*/30"),
                          id="post_saver.scripts.subreddit_scraper", replace_existing=True, max_instances=1)
        scheduler.add_job(genkan_website_scraper, trigger=CronTrigger(hour="*/3"),
                          id="post_saver.scripts.genkan_website_scraper", replace_existing=True, max_instances=1)
        scheduler.add_job(delete_old_posts, trigger=CronTrigger(day_of_week=0, hour="00", minute="00"),
                          id="post_saver.scripts.delete_old_posts", replace_existing=True, max_instances=1)
        scheduler.add_job(delete_old_seen_saved_posts, trigger=CronTrigger(day="1,16", hour="00", minute="00"),
                          id="post_saver.scripts.delete_old_seen_saved_posts", weeks=2, replace_existing=True, max_instances=1)

        scheduler.start()
        self.stdout.write(self.style.SUCCESS('Jobs scheduled.'))
