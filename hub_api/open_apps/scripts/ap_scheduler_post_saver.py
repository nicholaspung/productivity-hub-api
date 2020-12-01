from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from open_apps.scripts.post_saver import (delete_old_posts,
                                          delete_old_seen_saved_posts,
                                          genkan_website_scraper,
                                          subreddit_scraper)

job_defaults = {
    'max_instances': 1,
    'replace_existing': True
}
scheduler = BackgroundScheduler(
    timezone=settings.TIME_ZONE, job_defaults=job_defaults)
scheduler.add_jobstore(DjangoJobStore(), "default")


@scheduler.scheduled_job('interval', id='post_saver.scripts.subreddit_scraper', minutes=30)
def dev_subreddit_scraper():
    subreddit_scraper()


@scheduler.scheduled_job('interval', id='post_saver.scripts.genkan_website_scraper', hours=3)
def dev_genkan_website_scraper():
    genkan_website_scraper()


@scheduler.scheduled_job('interval', id='post_saver.scripts.delete_old_posts', weeks=1)
def dev_delete_old_posts():
    delete_old_posts()


@scheduler.scheduled_job('interval', id='post_saver.scripts.delete_old_seen_saved_posts', weeks=2)
def dev_delete_old_seen_saved_posts():
    delete_old_seen_saved_posts()

# Executes when server starts
# subreddit_scraper()
# genkan_website_scraper()
