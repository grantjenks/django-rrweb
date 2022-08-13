import datetime as dt

from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils import timezone as tz
from django.utils.html import format_html

from .models import Event, Session


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'kind', 'timestamp']
    list_select_related = ['session']
    readonly_fields = ['session']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        'create_time',
        'key',
        'event_duration',
        'event_count',
        'event_data_size',
        'event_min_timestamp',
        'event_max_timestamp',
        'link_view',
    ]

    fields = [
        'create_time',
        'key',
        'event_duration',
        'event_count',
        'event_data_size',
        'event_min_timestamp',
        'event_max_timestamp',
        'link_view',
    ]

    readonly_fields = fields

    def get_queryset(self, request):
        queryset = super().get_queryset(request).with_event_data()
        return queryset

    @admin.display(
        description='Event Duration',
        ordering='event_duration_num',
    )
    def event_duration(self, obj):
        return obj.event_duration_num

    @admin.display(
        description='Event Count',
        ordering='event_count_num',
    )
    def event_count(self, obj):
        return obj.event_count_num

    @admin.display(
        description='Event Data Size',
        ordering='event_data_size_num',
    )
    def event_data_size(self, obj):
        return obj.event_data_size_num

    @admin.display(
        description='Event Min Timestamp',
        ordering='event_min_timestamp_num',
    )
    def event_min_timestamp(self, obj):
        event_time = tz.make_aware(
            dt.datetime.fromtimestamp(obj.event_min_timestamp_num / 1000)
        )
        return event_time

    @admin.display(
        description='Event Max Timestamp',
        ordering='event_max_timestamp_num',
    )
    def event_max_timestamp(self, obj):
        event_time = tz.make_aware(
            dt.datetime.fromtimestamp(obj.event_max_timestamp_num / 1000)
        )
        return event_time

    @admin.display(
        description='View',
    )
    def link_view(self, obj):
        url = reverse(
            'admin:django-rrweb-session-replay',
            kwargs={'session_id': obj.id},
        )
        return format_html('<a href="{url}">view</a>', url=url)

    def replay_view(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        events = session.events.order_by('timestamp')
        context = dict(
            self.admin_site.each_context(request),
            events=events,
            session=session,
        )
        return render(request, 'django-rrweb/session-replay.html', context)

    def get_urls(self):
        urls = super().get_urls()
        replay_path = path(
            '<session_id>/replay/',
            self.replay_view,
            name='django-rrweb-session-replay',
        )
        urls.insert(0, replay_path)
        return urls
