from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
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
        'link_view',
        'link_delete',
    ]

    fields = [
        'session_key',
        'create_time',
        'user',
        'timestamp',
        'duration',
        'event_count',
        'event_size',
        'link_view',
        'link_delete',
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
    def link_view(self, obj):
        url = reverse(
            'admin:rrweb-session-replay',
            kwargs={'session_key': obj.session_key},
        )
        return format_html('<a href="{url}">view</a>', url=url)

    @admin.display(
        description='Delete',
        ordering='session_key',
    )
    def link_delete(self, obj):
        url = reverse(
            'admin:rrweb-session-delete',
            kwargs={'session_key': obj.session_key},
        )
        return format_html('<a href="{url}">delete</a>', url=url)

    def delete_view(self, request, session_key):
        session = get_object_or_404(Session, session_key=session_key)
        if request.method == 'POST':
            events = Event.objects.filter(session_key=session_key)
            events.delete()
            return redirect('admin:django_rrweb_session_changelist')
        context = dict(
            self.admin_site.each_context(request),
            session=session,
        )
        return render(request, 'django-rrweb/session-delete.html', context)

    def replay_view(self, request, session_key):
        session = get_object_or_404(Session, session_key=session_key)
        events = Event.objects.filter(session_key=session_key).order_by('id')
        context = dict(
            self.admin_site.each_context(request),
            events=events,
            session=session,
        )
        return render(request, 'django-rrweb/session-replay.html', context)

    def get_urls(self):
        urls = super().get_urls()
        delete_path = path(
            '<session_key>/delete/',
            self.delete_view,
            name='rrweb-session-delete',
        )
        replay_path = path(
            '<session_key>/replay/',
            self.replay_view,
            name='rrweb-session-replay',
        )
        return [delete_path, replay_path] + urls
