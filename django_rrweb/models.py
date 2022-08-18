import datetime as dt
import uuid

from django.db import models
from django.db.models import functions
from django.utils import timezone as tz


def _make_key():
    return str(uuid.uuid4()).replace('-', '')


class SessionQuerySet(models.QuerySet):
    def with_extras(self):
        queryset = (
            self.annotate(
                page_count_num=models.Count('pages__id', distinct=True)
            )
            .annotate(event_count_num=models.Count('pages__events__id'))
            .annotate(
                event_duration_num=functions.Coalesce(
                    models.Max('pages__events__timestamp')
                    - models.Min('pages__events__timestamp'),
                    0,
                )
            )
            .annotate(
                event_data_length_num=functions.Coalesce(
                    models.Sum(functions.Length('pages__events__data')), 0
                )
            )
            .annotate(
                event_timestamp_min_num=models.Min('pages__events__timestamp')
            )
            .annotate(
                event_timestamp_max_num=models.Max('pages__events__timestamp')
            )
        )
        return queryset


class Session(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    key = models.CharField(default=_make_key, max_length=100, unique=True)
    notes = models.TextField(blank=True, default='')

    make_key = staticmethod(_make_key)

    objects = SessionQuerySet.as_manager()

    def __str__(self):
        return self.key


class PageQuerySet(models.QuerySet):
    def with_extras(self):
        queryset = (
            self.annotate(event_count_num=models.Count('events__id'))
            .annotate(
                event_duration_num=functions.Coalesce(
                    models.Max('events__timestamp')
                    - models.Min('events__timestamp'),
                    0,
                )
            )
            .annotate(
                event_data_length_num=functions.Coalesce(
                    models.Sum(functions.Length('events__data')), 0
                )
            )
            .annotate(event_timestamp_min_num=models.Min('events__timestamp'))
            .annotate(event_timestamp_max_num=models.Max('events__timestamp'))
        )
        return queryset


class Page(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    key = models.CharField(default=_make_key, max_length=100, unique=True)
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='pages',
    )
    notes = models.TextField(blank=True, default='')

    make_key = staticmethod(_make_key)

    objects = PageQuerySet.as_manager()

    def __str__(self):
        return self.key


class EventQuerySet(models.QuerySet):
    def with_extras(self):
        queryset = self.annotate(data_length_num=functions.Length('data'))
        return queryset


class Event(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='events',
    )
    kind = models.SmallIntegerField()
    data = models.TextField(blank=True)
    timestamp = models.BigIntegerField()

    objects = EventQuerySet.as_manager()

    @property
    def datetime(self):
        return self.timestamp_to_datetime()

    def timestamp_to_datetime(self):
        timestamp = self.timestamp if isinstance(self, Event) else self
        datetime = tz.make_aware(dt.datetime.fromtimestamp(timestamp / 1000))
        return datetime

    def __str__(self):
        return f'#{self.id} @ {self.timestamp}'
