from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from timesync.pymesync import pymesync

import requests
import unittest
import json
import mock

class TimeSubmissionTestCase(TestCase):
    
    def setUp(self):
        self.Client = Client()
        baseurl = "http://140.211.168.211/v1"
        self.ts = pymesync.TimeSync(baseurl)
        self.ts.user = "test"
        self.ts.password = "test"
        self.auth_type = "password"
        self.ts.token = "TESTTOEKN"

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
                    'http://www.github.com',
                    'date_worked': '2015-5-20'}

        self.ts.create_time(new_time)

        self.ts._create_or_update.assert_called_with(new_time, None, "time", "times")

        #pymesync.TimeSync.create_time.assert_called_with(new_time)

        #resp = self.client.post(reverse('time-submission'), new_time)
        #print resp

        #time = new_time

        #for field in new_time:
            #self.assertIn(resp[field], new_time[field])
