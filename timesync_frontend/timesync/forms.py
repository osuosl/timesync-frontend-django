from django import forms

class TimeSelectionForm(forms.Form):
    project = forms.CharField(label='Project', required=False)
    user = forms.CharField(label='User', required=False)
    activities = forms.CharField(label='Activities', required=False)
    issue_uri = forms.URLField(label='Issue URI', required=False)
    start = forms.CharField(label='Start', required=False)
    end = forms.CharField(label='End', required=False)
    revisions = forms.CharField(label='Revisions', required=False)
    deleted = forms.CharField(label='Deleted', required=False)
