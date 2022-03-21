from django.core.management.base import BaseCommand
from open_apps.scripts.post_saver_scripts import subreddit_scraper, genkan_website_scraper, website_scraper_1, website_scraper_2, website_scraper_3, website_scraper_4


class Command(BaseCommand):
    args = ''
    help = 'Run every 30 minutes. Currently scrapes subreddit.'

    def handle(self, *args, **options):
        subreddit_scraper()
        genkan_website_scraper()
        website_scraper_1()
        website_scraper_2()
        website_scraper_3()
        website_scraper_4()
