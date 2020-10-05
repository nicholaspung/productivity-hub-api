from datetime import date, datetime, timedelta

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from django import db
from django.conf import settings
from django.db.utils import IntegrityError
from django_apscheduler.jobstores import DjangoJobStore, register_job

from post_saver.models import Post, SavedPost

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, 'interval', minutes=30, replace_existing=True)
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


# Executes when server starts
# subreddit_scraper()


@register_job(scheduler, 'interval', hours=3, replace_existing=True)
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


# Executes when server starts
# genkan_website_scraper()


@register_job(scheduler, 'interval', weeks=1, replace_existing=True)
def delete_old_posts():
    """
    This job deletes posts that are older than 1 week
    """
    one_week_ago = date.today() - timedelta(days=7)
    thirty_days_ago = date.today() - timedelta(days=30)
    Post.objects.filter(date__range=(
        thirty_days_ago, one_week_ago)).delete()

    db.connections.close_all()


@register_job(scheduler, 'interval', weeks=2, replace_existing=True)
def delete_old_seen_saved_posts():
    '''
    This job deletes old seen saved posts that older than 2 weeks
    '''
    two_weeks_ago = date.today() - timedelta(days=14)
    thirty_days_ago = date.today() - timedelta(days=30)
    SavedPost.objects.filter(date__range=(
        thirty_days_ago, two_weeks_ago)).delete()

    db.connections.close_all()
