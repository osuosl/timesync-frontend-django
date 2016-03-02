from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^time-submission', views.time_submission, name='time-submission'),
    url(r'^login', views.login, name='login'),
    url(r'^get-times', views.get_times, name='get-times'),
    url(r'^select-times', views.get_times, name='select-times'),
]
