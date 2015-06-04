from django.conf.urls import *
import views

urlpatterns = patterns('',
                       (r'^$', views.main_page),
                       (r'registro', views.registro),
                       (r'crearAsamblea', views.crear_asamblea),
                       (r'test_facebook', views.facebook_test),
                       )
