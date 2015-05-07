'''
Created on 25/11/2014

@author: silt
'''
from django.conf.urls import *
import views

urlpatterns = patterns('',
                       (r'^$', views.main_page),
                       (r'registro', views.registro),
                       (r'test_facebook', views.facebook_test),
                       )
