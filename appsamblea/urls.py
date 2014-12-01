from django.conf.urls import *
from django.contrib import admin

urlpatterns = patterns('',
    (r'^', include('guestbook.urls')),
)
