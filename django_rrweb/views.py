import json
from uuid import uuid4

from django.http import HttpResponse
from django.shortcuts import render

from .models import Event


def record_events(request):
    """Record events"""
    obj = json.load(request)
    assert obj['sessionKey']
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


def record_script(request):
    """Record script"""
    session_key = request.session.get('rrweb_session_key')
    if session_key is None:
        request.session['rrweb_session_key'] = str(uuid4())
    return render(
        request,
        'django-rrweb/record-script.js',
        content_type='application/javascript',
    )
