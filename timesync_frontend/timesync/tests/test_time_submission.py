from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class TimeSubmissionTestCase(TestCase):
    
    def setUp(self):
        self.Client = Client()

    def test_url_endpoint(self):
        url = reverse('submission')
        self.assertEqual(url, '/timesync/submission')

    def test_form_fields(self):
        response = self.client.get(reverse('submission'))
        print response

        fields = {'duration': 'input', 'user': 'input', 'project': 'input',
                  'activities': 'input', 'notes': 'textarea', 'issue_uri':
                  'input', 'date_worked': 'input'}
        form = response.context
        print form
        print response['notes']

        for field in fields:
            self.assertIn(fields[field], str(response[field]))

    def test_successful_time_creation(self):
        new_time = {'duration': '5', 'user': 'test', 'project': 'gwm',
                    'activities': 'docs', 'notes': '', 'issue_uri': '',
                    'date_worked': '2015-5-20'}

        self.client.post(reverse('submission'), new_time)

        time = new_time

        for field in new_time:
            self.assertIn(time[field], new_time[field])
