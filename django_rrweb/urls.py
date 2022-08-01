from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record),
    path('replay/<session_key>/', views.replay),
]
