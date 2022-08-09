from django.db import models
from django.db.models import Sum
from django.db.models.functions import Length


class Session(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    def min_timestamp(self):
        timestamp = (
            self.events.order_by('timestamp')
            .values_list('timestamp', flat=True)
            .first()
        )
        return timestamp or 0

    def max_timestamp(self):
        timestamp = (
            self.events.order_by('-timestamp')
            .values_list('timestamp', flat=True)
            .first()
        )
        return timestamp or 0

    def duration(self):
        return self.max_timestamp() - self.min_timestamp()

    def event_count(self):
        return self.events.count()

    def event_data_size(self):
        return self.events.aggregate(size=Sum(Length('data')))['size']

    def __str__(self):
        return f'#{self.id} @ {self.create_time}'


class Event(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='events',
    )
    kind = models.SmallIntegerField()
    data = models.TextField(blank=True)
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'#{self.id} @ {self.timestamp}'
