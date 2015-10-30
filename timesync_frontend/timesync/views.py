from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from forms import TimeSubmissionForm
# Create your views here.

def time_submission(request):
    if request.method == 'POST':
        form = TimeSubmissionForm(request.POST)
        
        if form.is_valid():
            return HttpResponseRedirect('/timesync/submitted/')
    else:
        form = TimeSubmissionForm()

    print form

    return render(request, 'timesync/time_submission_form.html', {'form': form})

def submitted(request):
    return render(request, 'timesync/submitted.html')
