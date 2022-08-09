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
    session = _get_session(request)
    obj = json.load(request)
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


def _get_session(request):
    session_id = request.session.get('django_rrweb_session_id')
    if session_id is None:
        session = _new_session(request)
    else:
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            session = _new_session(request)
    timestamp = session.max_timestamp()
    if not timestamp:
        return session
    event_time = tz.make_aware(dt.datetime.fromtimestamp(timestamp / 1000))
    if tz.now() - event_time > dt.timedelta(minutes=10):
        session = _new_session(request)
    return session


def _new_session(request):
    session = Session()
    session.save()
    session_id = session.id
    request.session['django_rrweb_session_id'] = session_id
    return session


def record_script(request):
    """Record script"""
    _get_session(request)
    return render(
        request,
        'django-rrweb/record-script.js',
        content_type='application/javascript',
    )
