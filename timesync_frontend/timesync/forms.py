from django import forms

class TimeSubmissionForm(forms.Form): 
    duration = forms.CharField(label='Duration')
    user = forms.CharField(label='User')
    project = forms.CharField(label='Project')
    activities = forms.CharField(label='Activities')
    notes = forms.CharField(label='Notes')
    issue_uri = forms.CharField(label='Issue URI')
    date_worked = forms.CharField(label='Date Worked')

    class Meta:
        fields = ['duration', 'user', 'project', 'activities', 'notes', 'issue_uri', 'date_worked']

        exclude = ('podcast', 'size', 'length', 'part', 'mime_type')
