from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from timesync.forms import TimeSubmissionForm, LoginForm, TimeSelectionForm
import pymesync
from django.core.urlresolvers import reverse

import json

def time_submission(request):
    #print request.session
    if not 'ts' in request.session:
        request.session['source'] = 'time-submission'
        return redirect(login)
    else:
        ts = pymesync.TimeSync('http://timesync-staging.osuosl.org/v1',
                token=request.session['ts'])

    #Get list of projects
    projects = ts.get_projects()
    if 'error' in projects[0]:
        request.session['source'] = 'time-submission'
        return redirect(login)
    project_names = []

    for project in projects:
        project_names.append((project['name'], project['name']))

    if request.method == 'POST':
        form = TimeSubmissionForm(projects=project_names, data=request.POST)

        if form.is_valid():
            for item in form.cleaned_data:
                params[item] = form.cleaned_data[item]

            params = {
                'duration': form.cleaned_data['duration'],
                'user': form.cleaned_data['user'],
                'project': form.cleaned_data['project'],
                'activities': form.cleaned_data['activities'],
                'notes': form.cleaned_data['notes'],
                'issue_uri': form.cleaned_data['issue_uri'],
                'date_worked': form.cleaned_data['date_worked'],
            }

            #Have to submit a slug
            for project in projects:
                if project['name'] == params['project']:
                    params['project'] = project['slugs'][0]

            #Deal with multiple activities
            params['activities'] = params['activities'].split(',')
            params['activities'] = [activity.strip() for activity in
                params['activities']]

            resp = ts.create_time(params)
            resp = resp[0]

            #Make prettier
            for key, value in resp.iteritems():
                resp[key.replace('_', ' ').title()] = resp.pop(key)

            #Return the response
            return render(request, 'timesync/time_submission_form.html',
                {'form': form, 'time': resp})
    else:
        form = TimeSubmissionForm(project_names)

    return render(request, 'timesync/time_submission_form.html', {'form': form,
        'time': ''})

def login(request):
    #print request.path
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            ts = pymesync.TimeSync('http://timesync-staging.osuosl.org/v1')
            ts.authenticate(form.cleaned_data['username'],
                form.cleaned_data['password'], "password")

            request.session['ts'] = ts.token
            return redirect(request.session['source'])
    else:
        form = LoginForm()
    return render(request, 'timesync/login.html', {'form': form})

def get_times(request):
    if not 'ts' in request.session:
        request.session['source'] = 'select-times'
        return redirect(login)
    else:
        ts = pymesync.TimeSync('http://timesync-staging.osuosl.org/v1',
                token=request.session['ts'])

    projects = ts.get_projects()
    if 'error' in projects[0]:
        request.session['source'] = 'select-times'
        return redirect(login)
    project_names = []

    for project in projects:
        project_names.append((project['name'], project['name']))

    if request.method == 'POST':
        form = TimeSelectionForm(projects=project_names, data=request.POST)
        if form.is_valid():
            params = dict()

            for item in form.cleaned_data:
                if form.cleaned_data[item]:
                    params[item] = form.cleaned_data[item]

            #Have to submit a slug
            if 'project' in params:
                for project in projects:
                    if project['name'] == params['project']:
                        params['project'] = [project['slugs'][0]]

            #Deal with multiple activities
            if 'activity' in params:
                params['activity'] = params['activity'].split(',')
                params['activity'] = [activity.strip() for activity in
                    params['activity']]

            if 'user' in params:
                params['user'] = params['user'].split(',')
                params['user'] = [activity.strip() for activity in
                    params['user']]

            resp = ts.get_times(params)
            return render(request, 'timesync/get_times.html', {'form': form,
                'times': resp})
    else:
        form = TimeSelectionForm(project_names)

    return render(request, 'timesync/get_times.html', {'form': form})
