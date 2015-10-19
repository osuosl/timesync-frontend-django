from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def submission(request):
    template = loader.get_template('timesync/time_submission_form.html')
    return HttpResponse(template.render())
    #return render(request, 'timesync/submission.html')
