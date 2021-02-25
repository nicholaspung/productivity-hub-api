from django.core.management.base import BaseCommand
from open_apps.scripts.post_saver_scripts import genkan_website_scraper


class Command(BaseCommand):
    args = ''
    help = 'Run every 30 minutes. Currently scrapes subreddit.'

    def handle(self, *args, **options):
        genkan_website_scraper()
