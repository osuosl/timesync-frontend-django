from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^submission', views.submission, name='submission'),
]
