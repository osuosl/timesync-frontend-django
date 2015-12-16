from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from timesync.forms import TimeSubmissionForm
from timesync.pymesync import pymesync

import json

def time_submission(request):
    ts = pymesync.TimeSync('http://140.211.168.211/v1',
                           password="test",
                           user="test",
                           auth_type="password")

    #Get list of projects
    projects = ts.get_projects()
    project_names = []

    for project in projects:
        project_names.append((project['name'], project['name']))

    if request.method == 'POST':
        form = TimeSubmissionForm(projects=project_names, data=request.POST)
        
        if form.is_valid():
            params = {
                'duration': form.cleaned_data['duration'],
                'user': form.cleaned_data['user'],
                'project': form.cleaned_data['project'],
                'activities': [form.cleaned_data['activities']],
                'notes': form.cleaned_data['notes'],
                'issue_uri': form.cleaned_data['issue_uri'],
                'date_worked': form.cleaned_data['date_worked'],
            }
            #Make date json serializable
            params['date_worked'] = params['date_worked'].strftime('%Y-%m-%d')
 
            resp = HttpResponse()
            resp = ts.send_time(params)
 
            #TODO
            #Format resp somehow

            return render(request, 'timesync/time_submission_form.html',
                    {'form': form, 'time': resp})
    else:
        form = TimeSubmissionForm(project_names)

    return render(request, 'timesync/time_submission_form.html', {'form': form,
            'time': ''})

def submitted(request):
    return render(request, 'timesync/submitted.html', {'time': time})
