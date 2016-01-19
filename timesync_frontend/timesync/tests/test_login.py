from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from timesync.pymesync import pymesync
from timesync.forms import LoginForm
from timesync.views import login
