'''
Created on 25/11/2014

@author: silt
'''
from django.conf.urls import *
from main_appsamblea.views import main_page

urlpatterns = patterns('',
                       (r'^$', main_page),
                       )
