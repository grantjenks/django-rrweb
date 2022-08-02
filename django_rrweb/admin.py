from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Event, Session


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['create_time', 'user', 'session_key']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        'create_time',
        'session_key',
        'user',
        'duration',
        'event_count',
        'event_size',
        'replay',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(
        description='View',
        ordering='session_key',
    )
    def replay(self, obj):
        url = reverse(
            'rrweb-replay-session',
            kwargs={'session_key': obj.session_key},
        )
        return format_html('<a href="{url}">view</a>', url=url)
