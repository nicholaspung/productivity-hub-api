from datetime import date, datetime, timedelta

import requests
# from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from django import db
# from django.conf import settings
from django.db.utils import IntegrityError
# from django_apscheduler.jobstores import DjangoJobStore

from post_saver.models import Post, SavedPost

# job_defaults = {
#     'max_instances': 1,
#     'replace_existing': True
# }
# scheduler = BackgroundScheduler(
#     timezone=settings.TIME_ZONE, job_defaults=job_defaults)
# scheduler.add_jobstore(DjangoJobStore(), "default")


# @scheduler.scheduled_job('interval', id='post_saver.scripts.subreddit_scraper', minutes=30)
def subreddit_scraper():
    '''
    This job scrapes subreddits to grab posts and put into Post table
    '''
    time = datetime.now().isoformat()
    subreddits = ['manga']
    for subreddit in subreddits:
        try:
            url = f"https://www.reddit.com/r/{subreddit}.json"
            subreddit_data = requests.get(
                url, headers={'User-Agent': f'your bot {time}'}).json()
            if 'message' in subreddit_data:
                print(subreddit_data['message'])
                return
            post_list = subreddit_data['data']['children']
            for post in post_list:
                post_data = post['data']
                post_obj = {
                    'reddit_id': post_data['id'],
                    'title': post_data['title'],
                    'url': post_data['url']
                }
                try:
                    Post.objects.get_or_create(
                        reddit_id=post_obj['reddit_id'], title=post_obj['title'], url=post_obj['url'])
                except IntegrityError as e:
                    continue
        except requests.exceptions.RequestException as e:
            return

    db.connections.close_all()


# @scheduler.scheduled_job('interval', id='post_saver.scripts.genkan_website_scraper', hours=3)
def genkan_website_scraper():
    '''
    This job scrapes 'genkan' websites to grab titles put into Post table
    '''
    urls = ['https://leviatanscans.com/latest',
            'https://reaperscans.com/latest',
            'https://zeroscans.com/latest',
            'https://skscans.com/latest',
            'https://methodscans.com/latest']
    for url in urls:
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, "html.parser")
            titles = soup.select('.row.mb-4 > div')
            for title in titles:
                image_content = title.select('.badge.badge-md')
                title_content = title.select('.list-title.ajax')
                chapter = image_content[0].contents[0].replace("\n", "")
                manga_title = title_content[0].contents[0].replace("\n", "")
                url = image_content[0].parent['href']
                final_title = f"{manga_title} {chapter}"
                post_obj = {
                    'title': final_title,
                    'url': url
                }
                try:
                    Post.objects.get_or_create(
                        title=post_obj['title'], url=post_obj['url'])
                except IntegrityError as e:
                    continue
        except requests.exceptions.RequestException as e:
            return

    db.connections.close_all()


# @scheduler.scheduled_job('interval', id='post_saver.scripts.delete_old_posts', weeks=1)
def delete_old_posts():
    """
    This job deletes posts that are older than 1 week
    """
    one_week_ago = date.today() - timedelta(days=7)
    thirty_days_ago = date.today() - timedelta(days=30)
    Post.objects.filter(date__range=(
        thirty_days_ago, one_week_ago)).delete()

    db.connections.close_all()


# @scheduler.scheduled_job('interval', id='post_saver.scripts.delete_old_seen_saved_posts', weeks=2)
def delete_old_seen_saved_posts():
    '''
    This job deletes old seen saved posts that older than 2 weeks
    '''
    two_weeks_ago = date.today() - timedelta(days=14)
    thirty_days_ago = date.today() - timedelta(days=30)
    SavedPost.objects.filter(date__range=(
        thirty_days_ago, two_weeks_ago)).delete()

    db.connections.close_all()

# Executes when server starts
# subreddit_scraper()
# genkan_website_scraper()
