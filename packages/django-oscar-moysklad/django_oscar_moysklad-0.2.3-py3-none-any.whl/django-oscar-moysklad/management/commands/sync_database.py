from django.conf import settings

from django.core.management.base import BaseCommand



class Command(BaseCommand):
    def handle(self, **options):
        print('Initialize moysklad')
        from tasks import initial_task
        initial_task()
