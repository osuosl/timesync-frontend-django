from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^submit-times', views.submit_times, name='submit-times'),
    url(r'^login', views.login, name='login'),
    url(r'^view-times', views.view_times, name='view-times'),
]
