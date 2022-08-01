from django.contrib import admin

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
    ]

    def has_change_permission(self, request, obj=None):
        return False
