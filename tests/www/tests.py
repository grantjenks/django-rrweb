import json

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from django_rrweb.models import Event

pytestmark = pytest.mark.django_db


class ReplayTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='password',
        )

    def test_backend(self):
        response = self.client.get('/backend/login/')
        assert response

    def test_record(self):
        event = {
            'sessionKey': 'abc',
            'rrwebEvents': [
                {
                    'type': 0,
                    'data': 'event data',
                    'timestamp': 123456789,
                },
                {
                    'type': 1,
                    'data': 'more event data',
                    'timestamp': 123456790,
                },
            ],
        }
        response = self.client.post(
            '/backend/rrweb/record/',
            event,
            content_type='application/json',
        )
        assert response

    def test_admin_session(self):
        self.test_record()
        self.client.force_login(self.user)
        response = self.client.get('/backend/django_rrweb/session/')
        assert response

    def test_admin_session_replay(self):
        self.test_record()
        self.client.force_login(self.user)
        response = self.client.get('/backend/django_rrweb/session/abc/replay/')
        assert response

    def test_admin_session_delete(self):
        self.test_record()
        assert Event.objects.all().count() == 2
        self.client.force_login(self.user)
        response = self.client.get('/backend/django_rrweb/session/abc/delete/')
        assert response
        response = self.client.post(
            '/backend/django_rrweb/session/abc/delete/'
        )
        assert response
        assert Event.objects.all().count() == 0
