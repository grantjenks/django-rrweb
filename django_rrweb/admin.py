import datetime as dt

from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Event, Session


def _three_sig_figs(num):
    scales = [
        (1e11, 1e9, 0, 'G'),
        (1e10, 1e9, 1, 'G'),
        (1e9, 1e9, 2, 'G'),
        (1e8, 1e6, 0, 'M'),
        (1e7, 1e6, 1, 'M'),
        (1e6, 1e6, 2, 'M'),
        (1e5, 1e3, 0, 'K'),
        (1e4, 1e3, 1, 'K'),
        (1e3, 1e3, 2, 'K'),
        (0, 1, 0, ''),
    ]
    for limit, scale, digits, magnitude in scales:
        if limit <= num:
            break
    return f'{round(num / scale, digits):.{digits}f}{magnitude}'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'kind', 'timestamp', 'data_length']
    list_select_related = ['session']
    readonly_fields = [
        'id',
        'session',
        'kind',
        'timestamp',
        'data_length',
        'data',
    ]
    search_fields = ['session__key']

    def get_queryset(self, request):
        queryset = super().get_queryset(request).with_extras()
        return queryset

    @admin.display(
        description='Data Length',
        ordering='data_length_num',
    )
    def data_length(self, obj):
        return _three_sig_figs(obj.data_length_num)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        'key',
        'create_time',
        'event_duration',
        'event_count',
        'event_data_length',
        'event_timestamp_min',
        'event_timestamp_max',
        'link_replay',
        'link_events',
    ]

    fields = [
        'key',
        'create_time',
        'event_duration',
        'event_count',
        'event_data_length',
        'event_timestamp_min',
        'event_timestamp_max',
        'link_replay',
        'link_events',
    ]

    readonly_fields = fields

    def get_queryset(self, request):
        queryset = super().get_queryset(request).with_extras()
        return queryset

    @admin.display(
        description='Event Duration',
        ordering='event_duration_num',
    )
    def event_duration(self, obj):
        microseconds = obj.event_duration_num
        delta = dt.timedelta(seconds=microseconds / 1000)
        duration = str(delta)[:-3]
        return duration

    @admin.display(
        description='Event Count',
        ordering='event_count_num',
    )
    def event_count(self, obj):
        return _three_sig_figs(obj.event_count_num)

    @admin.display(
        description='Event Data Length',
        ordering='event_data_length_num',
    )
    def event_data_length(self, obj):
        return _three_sig_figs(obj.event_data_length_num)

    @admin.display(
        description='Event Timestamp Min',
        ordering='event_timestamp_min_num',
    )
    def event_timestamp_min(self, obj):
        if obj.event_timestamp_min_num is None:
            return '-'
        return Event.timestamp_to_datetime(obj.event_timestamp_min_num)

    @admin.display(
        description='Event Timestamp Max',
        ordering='event_timestamp_max_num',
    )
    def event_timestamp_max(self, obj):
        if obj.event_timestamp_max_num is None:
            return '-'
        return Event.timestamp_to_datetime(obj.event_timestamp_max_num)

    @admin.display(
        description='Replay',
    )
    def link_replay(self, obj):
        url = reverse(
            'admin:django-rrweb-session-replay',
            kwargs={'session_id': obj.id},
        )
        return format_html('<a href="{url}">replay</a>', url=url)

    def replay_view(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        events = session.events.order_by('timestamp')
        context = dict(
            self.admin_site.each_context(request),
            events=events,
            session=session,
        )
        return render(request, 'django-rrweb/session-replay.html', context)

    @admin.display(
        description='Events',
    )
    def link_events(self, obj):
        url = reverse('admin:django_rrweb_event_changelist')
        return format_html(
            '<a href="{url}?q={key}">events</a>', url=url, key=obj.key
        )

    def get_urls(self):
        urls = super().get_urls()
        replay_path = path(
            '<session_id>/replay/',
            self.replay_view,
            name='django-rrweb-session-replay',
        )
        urls.insert(0, replay_path)
        return urls
