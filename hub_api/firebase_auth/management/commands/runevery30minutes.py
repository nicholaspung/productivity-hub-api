from django.core.management.base import BaseCommand, CommandError
from post_saver.scripts import subreddit_scraper


class Command(BaseCommand):
    args = ''
    help = 'Run every 30 minutes. Currently scrapes subreddit.'

    def handle(self, *args, **options):
        subreddit_scraper()
