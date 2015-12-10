from django import forms

class TimeSubmissionForm(forms.Form):
    def __init__(self, projects, *args, **kwargs):
        super(TimeSubmissionForm, self).__init__(*args, **kwargs)
        print projects
        self.fields['project'] = forms.ChoiceField(choices=projects)

    duration = forms.CharField(label='Duration')
    user = forms.CharField(label='User')
    #project = forms.ChoiceField(label='Project')
    activities = forms.CharField(label='Activities')
    notes = forms.CharField(label='Notes')
    issue_uri = forms.URLField(label='Issue URI', 
        help_text='E.g. http://www.github.com')
    date_worked = forms.DateField(label='Date Worked',
        help_text='Year-Month-Day')

    """
    class Meta:
        fields = ['duration', 'user', 'project', 'activities', 'notes', 'issue_uri', 'date_worked']

        #exclude = ('podcast', 'size', 'length', 'part', 'mime_type')
    """
