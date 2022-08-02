from django.conf import settings
from django.db import models


class Event(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    kind = models.SmallIntegerField()
    data = models.TextField(blank=True)
    timestamp = models.BigIntegerField()
    session_key = models.CharField(max_length=100)


class Session(models.Model):
    session_key = models.CharField(primary_key=True, max_length=100)
    create_time = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    timestamp = models.BigIntegerField()
    duration = models.BigIntegerField()
    event_count = models.IntegerField()
    event_size = models.BigIntegerField()

    def __str__(self):
        return self.session_key

    class Meta:
        managed = False
