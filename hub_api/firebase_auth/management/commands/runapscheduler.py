from datetime import date, datetime, timedelta

import requests
from apscheduler.schedulers.background import BackgroundScheduler
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
        scheduler.add_job(prune_anonymous_users_in_firebase_and_django, 'interval',
                          id="firebase_auth.scripts.prune_anonymous_users_in_firebase_and_django", weeks=1, replace_existing=True, max_instances=1)
        scheduler.add_job(delete_old_job_executions, 'interval',
                          id="firebase_auth.scripts.delete_old_job_executions", weeks=1, replace_existing=True, max_instances=1)

        # post saver scripts
        scheduler.add_job(subreddit_scraper, 'interval',
                          id="post_saver.scripts.subreddit_scraper", minutes=30, replace_existing=True, max_instances=1)
        scheduler.add_job(genkan_website_scraper, 'interval',
                          id="post_saver.scripts.genkan_website_scraper", hours=3, replace_existing=True, max_instances=1)
        scheduler.add_job(delete_old_posts, 'interval',
                          id="post_saver.scripts.delete_old_posts", weeks=1, replace_existing=True, max_instances=1)
        scheduler.add_job(delete_old_seen_saved_posts, 'interval',
                          id="post_saver.scripts.delete_old_seen_saved_posts", weeks=2, replace_existing=True, max_instances=1)

        scheduler.start()
        self.stdout.write(self.style.SUCCESS('Jobs scheduled.'))
