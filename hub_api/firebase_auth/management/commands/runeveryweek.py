from django.core.management.base import BaseCommand, CommandError
from firebase_auth.scripts import prune_anonymous_users_in_firebase_and_django
from post_saver.scripts import delete_old_posts


class Command(BaseCommand):
    args = ''
    help = 'Run every week. Currently deletes old posts and prunes anonymous users in Firebase and Django.'

    def handle(self, *args, **options):
        delete_old_posts()
        prune_anonymous_users_in_firebase_and_django()
