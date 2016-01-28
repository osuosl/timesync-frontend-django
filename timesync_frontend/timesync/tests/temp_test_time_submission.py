from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from timesync.pymesync import pymesync
from timesync.forms import TimeSubmissionForm
from django.test.client import RequestFactory
from timesync.views import time_submission

import requests
import unittest
import json
import mock

class TimeSubmissionTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        baseurl = "http://140.211.168.211/v1"
        self.ts = pymesync.TimeSync(baseurl)
        self.actual_create_time = pymesync.TimeSync.create_time
        self.ts.user = "test"
        self.ts.password = "test"
        self.auth_type = "password"
        self.ts.token = "TESTTOKEN"

    def tearDown(self):
        del(self.ts)
        pymesync.TimeSync.create_time = self.actual_create_time

    def test_url_endpoint(self):
        url = reverse('time-submission')
        self.assertEqual(url, '/timesync/time-submission')

    def test_form_fields(self):
        response = self.client.get(reverse('time-submission'))

        fields = {'duration', 'user', 'project', 'activities', 'notes',
                  'issue_uri', 'date_worked'}
        form = response.context

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'timesync/time_submission_form.html')

        for field in fields:
            self.assertContains(response, field)

    def test_successful_time_creation(self):
        new_time = {'duration': '5', 'user': 'test', 'project': 'pymesync',
                    'activities': 'code', 'notes': 'note', 'issue_uri':
                    'http://www.github.com', 'date_worked': '2015-05-20'}

        self.ts._create_or_update = mock.Mock(self.ts._create_or_update)

        self.ts.create_time(new_time)

        self.ts._create_or_update.assert_called_with(new_time, None, "time", "times")

    def test_form_submission(self):
        new_time = {'duration': 5, 'user': 'test', 'project': 'pymesync',
                    'activities': 'code', 'notes': 'note', 'issue_uri':
                    'http://www.github.com',
                    'date_worked': '2015-05-20'}

        rf = RequestFactory()
        post_request = rf.post(reverse('time-submission'), new_time)

        form = TimeSubmissionForm(projects=[('pymesync', 'pymesync')],
                data=post_request.POST)

        self.assertTrue(form.is_valid())

    def test_invalid_form_submission(self):
        new_time = {'duration': 5, 'project': 'pymesync',
                    'activities': 'code', 'notes': 'note', 'issue_uri':
                    'http://www.github.com',
                    'date_worked': '2015-05-20'}

        rf = RequestFactory()
        post_request = rf.post(reverse('time-submission'), new_time)

        form = TimeSubmissionForm(projects=[('pymesync', 'pymesync')],
                data=post_request.POST)

        self.assertFalse(form.is_valid())

    def test_pymesync(self):
        new_time = {'duration': 5, 'user': 'test', 'project': 'PymeSync',
                    'activities': ['code'], 'notes': 'note', 'issue_uri':
                    'http://www.github.com',
                    'date_worked': '2015-05-20'}

        rf = RequestFactory()
        post_request = rf.post(reverse('time-submission'), new_time)

        pymesync.TimeSync.create_time = mock.create_autospec(
                pymesync.TimeSync.create_time, return_value=[new_time])
        resp = time_submission(post_request)

        pymesync.TimeSync.create_time.assert_called_with(self.ts, new_time)
