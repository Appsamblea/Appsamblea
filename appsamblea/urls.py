from django.conf.urls import *
from django.contrib import admin

urlpatterns = patterns('',
    (r'^', include('main_appsamblea.urls')),
)
