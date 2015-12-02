from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get-times', views.get_times, name='get-times'),
    url(r'^select-times', views.get_times, name='select-times'),
]
