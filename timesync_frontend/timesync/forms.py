from django import forms

class TimeSubmissionForm(forms.Form):
    def __init__(self, projects, *args, **kwargs):
        super(TimeSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.ChoiceField(choices=projects)

    duration = forms.IntegerField(label='Duration')
    user = forms.CharField(label='User')
    project = forms.ChoiceField(label='Project')
    activities = forms.CharField(label='Activities', 
        help_text='Comma separated')
    notes = forms.CharField(label='Notes')
    issue_uri = forms.URLField(label='Issue URI', 
        help_text='E.g. http://www.github.com')
    date_worked = forms.CharField(label='Date Worked',
        help_text='Year-Month-Day')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())