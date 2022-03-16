from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup
from django import db
from django.db.utils import IntegrityError
from open_apps.models.post_saver import Post, SavedPost


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
                title = post_data['title'][:150]
                post_obj = {
                    'reddit_id': post_data['id'],
                    'title': title,
                    'url': post_data['url']
                }
                try:
                    Post.objects.get_or_create(**post_obj)
                except IntegrityError:
                    continue
        except requests.exceptions.RequestException:
            return

    db.connections.close_all()


def genkan_website_scraper():
    '''
    This job scrapes 'genkan' websites to grab titles put into Post table
    '''
    urls = ['https://zeroscans.com/latest']
    for url in urls:
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, "html.parser")
            titles = soup.select('.row.mb-4 > div')
            for title in titles:
                image_content = title.select('.badge.badge-md')
                title_content = title.select('.list-title.ajax')
                chapter = image_content[0].contents[0].replace("\n", "")
                manga_title = title_content[0].contents[0].replace("\n", "")[
                    :140]
                url = image_content[0].parent['href']
                final_title = f"{manga_title} {chapter}"
                post_obj = {
                    'title': final_title,
                    'url': url
                }
                try:
                    Post.objects.get_or_create(
                        title=post_obj['title'], url=post_obj['url'])
                except IntegrityError:
                    continue
        except requests.exceptions.RequestException:
            return

    db.connections.close_all()


def website_scraper_1():
    urls = ['https://reaperscans.com/latest-comic/']
    for url in urls:
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, "html.parser")
            titles = soup.select('.page-item-detail.manga')
            for title in titles:
                chapters = title.select(
                    '.item-summary > .list-chapter > .chapter-item.has-thumb.free-chap > .chapter.font-meta > .btn-link')
                manga_title = title.select(
                    '.item-summary > .post-title.font-title > .h5 > a')[0].contents[0]
                for chapter in chapters:
                    chapter_num = chapter.contents[0].split(' ')[2]
                    url = chapter['href']
                    final_title = f"{manga_title} Ch. {chapter_num}"
                    post_obj = {
                        'title': final_title,
                        'url': url
                    }
                    try:
                        Post.objects.get_or_create(
                            title=post_obj['title'], url=post_obj['url'])
                    except IntegrityError:
                        continue
        except requests.exceptions.RequestException:
            return
    db.connections.close_all()


def website_scraper_2():
    urls = ['https://luminousscans.com/series/?order=update',
            'https://www.asurascans.com/manga/?order=update',
            'https://alpha-scans.org/manga/?order=update'
            ]
    for url in urls:
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, "html.parser")
            titles = soup.select('.bs')
            for title in titles:
                url = title.select('.bsx > a')[0]['href']
                manga_title = title.select('.bsx > a')[0]['title']
                chapter = title.select('.bsx > a > .bigor > .adds > .epxs')[
                    0].contents[0]
                final_title = f"{manga_title} {chapter}"
                post_obj = {
                    'title': final_title,
                    'url': url
                }
                try:
                    Post.objects.get_or_create(
                        title=post_obj['title'], url=post_obj['url'])
                except IntegrityError:
                    continue
        except requests.exceptions.RequestException:
            return


def website_scraper_3():
    urls = ['https://flamescans.org/']
    for url in urls:
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, "html.parser")
            titles = soup.select('.bs.styletere')
            for title in titles:
                manga_title = title.select('.bsx > a')[0]['title']
                chapters = title.select('.bsx > .bigor > .chapter-list')

                if len(chapters) == 0:
                    continue

                for chapter in chapters:
                    chapter_num = chapter.select('.adds > .epxs')

                    if len(chapter_num) == 0:
                        continue

                    chapter_num_text = chapter_num[0].contents[0].replace(
                        '\n', '').split(' ')[1]
                    url = chapter.contents[1]['href']
                    final_title = f"{manga_title} Ch. {chapter_num_text}"
                    post_obj = {
                        'title': final_title,
                        'url': url
                    }
                    try:
                        Post.objects.get_or_create(
                            title=post_obj['title'], url=post_obj['url'])
                    except IntegrityError:
                        continue
        except requests.exceptions.RequestException:
            return


def website_scraper_4():
    urls = ['https://reader.kireicake.com/reader/']
    for url in urls:
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, "html.parser")
            titles = soup.select('.group')
            for title in titles:
                manga_title = title.select('.title > a')[0]['title']
                chapters = title.select('.element')

                for chapter in chapters:
                    chapter_num = chapter.select('.title > a')[0]['title']
                    url = chapter.select('.title > a')[0]['href']
                    final_title = f"{manga_title} {chapter_num}"
                    post_obj = {
                        'title': final_title,
                        'url': url
                    }

                    try:
                        Post.objects.get_or_create(
                            title=post_obj['title'], url=post_obj['url'])
                    except IntegrityError:
                        continue
        except requests.exceptions.RequestException:
            return


def delete_old_posts():
    """
    This job deletes posts that are older than 1 week
    """
    one_week_ago = date.today() - timedelta(days=7)
    Post.objects.filter(date__lte=one_week_ago).delete()

    db.connections.close_all()


def delete_old_seen_saved_posts():
    '''
    This job deletes old seen saved posts that older than 2 weeks
    '''
    two_weeks_ago = date.today() - timedelta(days=14)
    SavedPost.objects.filter(date__lte=two_weeks_ago, seen=True).delete()

    db.connections.close_all()
