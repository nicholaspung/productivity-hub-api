from django.core.management.base import BaseCommand
from open_apps.scripts.populate_db import populate_apps


class Command(BaseCommand):
    args = ''
    help = 'Run every 30 minutes. Currently scrapes subreddit.'

    def handle(self, *args, **options):
        populate_apps()
