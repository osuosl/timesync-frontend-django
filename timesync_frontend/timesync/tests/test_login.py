from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from timesync.pymesync import pymesync
from timesync.forms import LoginForm
from timesync.views import login
from django.conf import settings
from importlib import import_module
from django.contrib.sessions.backends.db import SessionStore

import requests
import json
import mock

class ModifySessionMixin(object):
    client = Client()

    def create_session(self):
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

class LoginTestCase(ModifySessionMixin, TestCase):

    def setUp(self):
        self.client = Client()
        baseurl = "http://140.211.168.211/v1"
        self.ts = pymesync.TimeSync(baseurl)
        self.ts.user = "test"
        self.ts.password = "test"
        self.auth_type = "password"
        self.ts.token = "TESTTOKEN"
        self.test = True

        # Set up session
        self.create_session()
        #self.session = SessionStore()
        #self.session.save()
        #self.client.session = SessionStore()
        #self.client.session['ts'] = self.ts.token
        #self.client.session.save()

        #engine = import_module(settings.SESSION_ENGINE)
        #self.client.session = engine.SessionStore()
        #self.client.session.save()
        #store = engine.SessionStore()
        #store.save()
        #self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_url_endpoint(self):
        url = reverse('login')
        self.assertEqual(url, '/timesync/login')

    def test_form_fields(self):
        response = self.client.get(reverse('login'))
        fields = {'username', 'password'}

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'timesync/login.html')

        for field in fields:
            self.assertContains(response, field)

    def test_expired_token_redirect(self):
        new_time = {'duration': '5', 'user': 'test', 'project': 'pymesync',
                'activities': 'code', 'notes': 'note', 'issue_uri':
                'http://www.github.com', 'date_worked': '2015-05-20'}

        #self.client.session['ts'] = self.ts
        #response = self.client.get(reverse('time-submission'))
        #print response
        #request.session['ts'] = self.ts

        """
        session = self.client.session
        session['ts'] = self.ts
        session.save()
        print session['ts']

        session = SessionStore()
        session['ts'] = self.ts.token
        session.save()

        print session
        """

        self.client.session['ts'] = self.ts.token
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        self.client.session.save()

        reponse = self.client.post(reverse('time-submission'), new_time)

        #print response
        #self.assertEqual(
