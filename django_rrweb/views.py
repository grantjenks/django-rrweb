import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Event, Session


def record(request):
    obj = json.load(request)
    events = [
        Event(
            user=None if request.user.is_anonymous else request.user,
            kind=event['type'],
            data=json.dumps(event['data']),
            timestamp=event['timestamp'],
            session_key=obj['sessionKey'],
        )
        for event in obj['rrwebEvents']
    ]
    Event.objects.bulk_create(events)
    return HttpResponse('OK', content_type='text/plain')


def replay(request, session_key):
    session = get_object_or_404(Session, session_key=session_key)
    events = Event.objects.filter(session_key=session_key)
    events = list(events.order_by('timestamp'))
    events = Event.objects.all().order_by('id')
    return render(request, 'django-rrweb/replay.html', {'events': events})
