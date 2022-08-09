from django.contrib import admin
from django.db.models import Count, Max, Min, Sum
from django.db.models.functions import Length
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Event, Session


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['session', 'timestamp']
    list_select_related = ['session']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        'create_time',
        'duration',
        'event_count',
        'event_data_size',
        'link_view',
    ]

    fields = [
        'create_time',
        'duration',
        'event_count',
        'event_data_size',
        'link_view',
    ]

    readonly_fields = fields

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = (
            queryset.annotate(event_count_num=Count('events__id'))
            .annotate(
                duration_num=(
                    Max('events__timestamp') - Min('events__timestamp')
                )
            )
            .annotate(event_data_size_num=Sum(Length('events__data')))
        )
        return queryset

    @admin.display(
        description='Duration',
        ordering='duration_num',
    )
    def duration(self, obj):
        return obj.duration()

    @admin.display(
        description='Event Count',
        ordering='event_count_num',
    )
    def event_count(self, obj):
        return obj.event_count()

    @admin.display(
        description='Event Data Size',
        ordering='event_data_size_num',
    )
    def event_data_size(self, obj):
        return obj.event_data_size()

    @admin.display(
        description='View',
        ordering='create_time',
    )
    def link_view(self, obj):
        url = reverse(
            'admin:django-rrweb-session-replay',
            kwargs={'session_id': obj.id},
        )
        return format_html('<a href="{url}">view</a>', url=url)

    def replay_view(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        events = session.events.order_by('id')
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
