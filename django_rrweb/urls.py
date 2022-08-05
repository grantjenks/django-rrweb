from django.urls import path

from . import views

urlpatterns = [
    path(
        'django_rrweb/record/events/',
        views.record_events,
        name='django-rrweb-record-events',
    ),
    path(
        'django_rrweb/record/script/',
        views.record_script,
        name='django-rrweb-record-script',
    ),
]
