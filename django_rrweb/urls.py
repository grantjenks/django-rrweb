from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record, name='rrweb-record'),
    path(
        'replay/<session_key>/',
        views.replay_session,
        name='rrweb-replay-session',
    ),
]
