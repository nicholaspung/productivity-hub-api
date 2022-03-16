from django.core.management.base import BaseCommand
from open_apps.scripts.trial import trial


class Command(BaseCommand):
    args = ''
    help = 'To run sample scripts for testing'

    def handle(self, *args, **options):
        trial()
