import datetime as dt
import logging
import time

from django.core.management.base import BaseCommand
from django.utils import timezone as tz

from ...models import Page, Session

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Purges pages and sessions'

    def add_arguments(self, parser):
        parser.add_argument('--delay', default=600, type=int)
        parser.add_argument('--limit', default=float('inf'), type=int)
        parser.add_argument('--max-age', default=7, type=int)

    def handle(self, *args, **options):
        delay = options['delay']
        limit = options['limit']
        max_age = dt.timedelta(days=options['max_age'])
        count = 0

        while True:
            now = tz.now()
            past = now - max_age
            sessions = Session.objects.filter(
                notes='',
                pages__notes='',
                create_time__lt=past,
            )
            log.warning('Deleting %s sessions', sessions.count())
            sessions.delete()
            pages = Page.objects.filter(
                notes='',
                session__notes='',
                create_time__lt=past,
            )
            log.warning('Deleting %s pages', pages.count())
            pages.delete()
            count += 1
            if count >= limit:
                break
            log.info('Sleeping for %s seconds', delay)
            time.sleep(delay)
