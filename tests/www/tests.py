import io

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from django_rrweb.models import Event, Page, Session

pytestmark = pytest.mark.django_db


class ReplayTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='password',
        )

    def test_record_script(self):
        self.assertFalse(self.client.session.get('django_rrweb_session_key'))
        response = self.client.get('/backend/django_rrweb/record/script/')
        self.assertEqual(response.status_code, 200)
        key = self.client.session['django_rrweb_session_key']
        self.assertTrue(key)
        response = self.client.get('/backend/django_rrweb/record/script/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(key, self.client.session['django_rrweb_session_key'])
        session = Session.objects.create(key=key)
        page = Page.objects.create(key=key, session=session)
        Event.objects.create(page=page, kind=0, data='', timestamp=1)
        response = self.client.get('/backend/django_rrweb/record/script/')
        self.assertEqual(response.status_code, 200)
        new_key = self.client.session['django_rrweb_session_key']
        self.assertNotEqual(key, new_key)

    def test_record(self):
        data = {
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
            'rrwebPageKey': 'test-page-key',
            'rrwebSessionKey': 'test-session-key',
        }
        response = self.client.post(
            '/backend/django_rrweb/record/events/',
            data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

    def test_record_get(self):
        response = self.client.get('/backend/django_rrweb/record/events/')
        self.assertEqual(response.status_code, 405)

    def test_admin_event(self):
        self.test_record()
        self.client.force_login(self.user)
        response = self.client.get('/backend/django_rrweb/event/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/backend/django_rrweb/event/1/change/')
        self.assertEqual(response.status_code, 200)

    def test_admin_page(self):
        self.test_record()
        self.client.force_login(self.user)
        response = self.client.get('/backend/django_rrweb/page/')
        self.assertEqual(response.status_code, 200)
        page_id = Page.objects.all().values_list('id', flat=True).first()
        url = f'/backend/django_rrweb/page/{page_id}/change/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_page_replay(self):
        self.test_record()
        self.client.force_login(self.user)
        page_id = Page.objects.all().values_list('id', flat=True).first()
        url = f'/backend/django_rrweb/page/{page_id}/replay/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_session(self):
        self.test_record()
        self.client.force_login(self.user)
        response = self.client.get('/backend/django_rrweb/session/')
        self.assertEqual(response.status_code, 200)
        session_id = Session.objects.all().values_list('id', flat=True).first()
        url = f'/backend/django_rrweb/session/{session_id}/change/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class RrwebPurgeTestCase(TestCase):
    def test_rrweb_purge(self):
        output = io.StringIO()
        args = 'rrwebpurge', '--limit', '2', '--delay', '1'
        call_command(*args, stdout=output)
        assert output.getvalue() == ''
