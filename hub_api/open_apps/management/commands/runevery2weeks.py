from django.core.management.base import BaseCommand
from open_apps.scripts.post_saver_scripts import delete_old_seen_saved_posts


class Command(BaseCommand):
    args = ''
    help = 'Run every 30 minutes. Currently scrapes subreddit.'

    def handle(self, *args, **options):
        delete_old_seen_saved_posts()
