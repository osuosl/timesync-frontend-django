from django import forms

class TimeSelectionForm(forms.Form):
    project = forms.CharField(label='Project')
    user = forms.CharField(label='User')
    activities = forms.CharField(label='Activities')
    issue_uri = forms.URLField(label='Issue URI')
    start = forms.CharField(label='Start')
    end = forms.CharField(label='End')
    revisions = forms.CharField(label='Revisions')
    deleted = forms.CharField(label='Deleted')
