import pytest
from django.contrib.auth.models import User
from django.test import TestCase

pytestmark = pytest.mark.django_db


class ReplayTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='password',
        )

    def test_record_script(self):
        response = self.client.get('/backend/django_rrweb/record/script/')
        self.assertEqual(response.status_code, 200)

    def test_record(self):
        data = {
            'rrwebSessionKey': 'abcdef0123456789',
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
            '/backend/django_rrweb/record/events/',
            data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/backend/django_rrweb/record/events/',
            data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_session(self):
        self.test_record()
        self.client.force_login(self.user)
        response = self.client.get('/backend/django_rrweb/session/')
        self.assertEqual(response.status_code, 200)

    def test_admin_session_replay(self):
        self.test_record()
        self.client.force_login(self.user)
        response = self.client.get('/backend/django_rrweb/session/1/replay/')
        self.assertEqual(response.status_code, 200)
