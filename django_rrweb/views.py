import datetime as dt
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone as tz
from django.views.decorators.csrf import csrf_exempt

from .models import Event, Session


@csrf_exempt
def record_events(request):
    """Record events"""
    if request.method != 'POST':
        return HttpResponse('ERROR: POST request required', status=405)
    obj = json.load(request)
    session, _ = Session.objects.get_or_create(key=obj['rrwebSessionKey'])
    events = [
        Event(
            kind=event['type'],
            data=json.dumps(event['data']),
            timestamp=event['timestamp'],
            session=session,
        )
        for event in obj['rrwebEvents']
    ]
    Event.objects.bulk_create(events)
    return HttpResponse('OK', content_type='text/plain')


def record_script(request):
    """Record script"""
    session_key = request.session.get('django_rrweb_session_key')
    if session_key is None:
        session_key = Session.make_key()
        request.session['django_rrweb_session_key'] = session_key
    else:
        event = (
            Event.objects.filter(session__key=session_key)
            .order_by('-timestamp')
            .only('timestamp')
            .first()
        )
        delta = dt.timedelta(minutes=10)
        update = event is not None and (tz.now() - event.datetime) > delta
        if update:
            session_key = Session.make_key()
            request.session['django_rrweb_session_key'] = session_key
    return render(
        request,
        'django-rrweb/record-script.js',
        {'session_key': session_key},
        content_type='application/javascript',
    )
