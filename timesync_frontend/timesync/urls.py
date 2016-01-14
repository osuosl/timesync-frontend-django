from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^time-submission', views.time_submission, name='time-submission'),
    url(r'^submitted', views.submitted, name='submitted'),
    url(r'^login', views.login, name='login'),
]
