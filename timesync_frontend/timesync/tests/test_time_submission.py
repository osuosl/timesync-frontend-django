from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class TimeSubmissionTestCase(TestCase):
    
    def setUp(self):
        self.Client = Client()

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
        new_time = {'duration': '5', 'user': 'test', 'project': 'gwm',
                    'activities': 'docs', 'notes': '', 'issue_uri': '',
                    'date_worked': '2015-5-20'}

        self.client.post(reverse('time-submission'), new_time)

        time = new_time

        for field in new_time:
            self.assertIn(time[field], new_time[field])
