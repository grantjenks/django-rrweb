import json
from uuid import uuid4

from django.http import HttpResponse

from .models import Event


def record(request):
    """Record event"""
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


def record_script(request):
    session_key = request.session.get('rrweb-session-key')
    if session_key is None:
        request.session['rrweb-session-key'] = str(uuid4())
    return render(request, 'django-rrweb/record-script.js')
