from django.shortcuts import render
from django.template import loader
from timesync.pymesync import pymesync
from timesync.forms import TimeSelectionForm

def get_times(request):
    ts = pymesync.TimeSync('http://140.211.168.211',
                           password="password",
                           user="example-user",
                           auth_type="password")

    if request.method == 'POST':
        form = TimeSelectionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['project']:
                resp = ts.get_times(project=form.cleaned_data['project'])
            elif form.cleaned_data['user']:
                resp = ts.get_times(user=form.cleaned_data['user'])
            elif form.cleaned_data['activities']:
                resp = ts.get_times(activity=form.cleaned_data['activities'])
            elif form.cleaned_data['issue_uri']:
                resp = ts.get_times(issue_uri=form.cleaned_data['issue_uri'])
            elif form.cleaned_data['issue_uri']:
               resp = ts.get_times(issue_uri=form.cleaned_data['issue_uri'])
            elif form.cleaned_data['issue_uri']:
               resp = ts.get_times(issue_uri=form.cleaned_data['issue_uri'])
            print resp

            return render(request, 'timesync/get_times.html', {'times': resp})
        else:
            print form.is_valid()
    else:
        form = TimeSelectionForm()

    return render(request, 'timesync/select_times.html', {'form': form})
