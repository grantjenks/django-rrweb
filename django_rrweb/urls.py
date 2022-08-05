from django.urls import path

from . import views

urlpatterns = [
    path('record/', views.record, name='rrweb-record'),
    path(
        'record/django-rrweb.js',
        views.record_script,
        name='rrweb-record-script',
    ),
]
