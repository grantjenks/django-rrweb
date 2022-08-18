import datetime as dt

from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Event, Page, Session


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
    list_display = [
        'id',
        'timestamp',
        'data_length',
        'kind',
        'page',
        'session',
    ]
    list_select_related = ['page', 'page__session']
    fields = list_display + ['data']
    readonly_fields = fields
    search_fields = ['page__key', 'page__session__key']
    ordering = ['-timestamp']

    def get_queryset(self, request):
        queryset = super().get_queryset(request).with_extras()
        return queryset

    @admin.display(
        description='Session',
        ordering='page__session__id',
    )
    def session(self, obj):
        return obj.page.session

    @admin.display(
        description='Data Length',
        ordering='data_length_num',
    )
    def data_length(self, obj):
        return _three_sig_figs(obj.data_length_num)


class EventMixin:
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
        description='Events',
    )
    def link_events(self, obj):
        url = reverse('admin:django_rrweb_event_changelist')
        return format_html(
            '<a href="{url}?q={key}">events</a>', url=url, key=obj.key
        )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin, EventMixin):
    list_display = [
        'key',
        'link_replay',
        'link_events',
        'create_time',
        'event_duration',
        'event_count',
        'event_data_length',
        'event_timestamp_min',
        'event_timestamp_max',
        'session',
    ]
    readonly_fields = list_display
    fields = readonly_fields + ['notes']
    ordering = ['-create_time']
    search_fields = ['key', 'session__key', 'notes']

    def get_queryset(self, request):
        queryset = super().get_queryset(request).with_extras()
        return queryset

    @admin.display(
        description='Replay',
    )
    def link_replay(self, obj):
        url = reverse(
            'admin:django-rrweb-page-replay',
            kwargs={'page_id': obj.id},
        )
        return format_html('<a href="{url}">replay</a>', url=url)

    def replay_view(self, request, page_id):
        page = get_object_or_404(Page, id=page_id)
        events = page.events.order_by('timestamp')
        context = dict(
            self.admin_site.each_context(request),
            events=events,
            page=page,
        )
        return render(request, 'django-rrweb/page-replay.html', context)

    def get_urls(self):
        urls = super().get_urls()
        replay_path = path(
            '<page_id>/replay/',
            self.replay_view,
            name='django-rrweb-page-replay',
        )
        urls.insert(0, replay_path)
        return urls


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin, EventMixin):
    list_display = [
        'key',
        'link_pages',
        'link_events',
        'create_time',
        'page_count',
        'event_duration',
        'event_count',
        'event_data_length',
        'event_timestamp_min',
        'event_timestamp_max',
    ]
    readonly_fields = list_display
    fields = readonly_fields + ['notes']
    ordering = ['-create_time']
    search_fields = ['key', 'notes']

    def get_queryset(self, request):
        queryset = super().get_queryset(request).with_extras()
        return queryset

    @admin.display(
        description='Page Count',
        ordering='page_count_num',
    )
    def page_count(self, obj):
        return _three_sig_figs(obj.page_count_num)

    @admin.display(
        description='Pages',
    )
    def link_pages(self, obj):
        url = reverse('admin:django_rrweb_page_changelist')
        return format_html(
            '<a href="{url}?q={key}">pages</a>', url=url, key=obj.key
        )
