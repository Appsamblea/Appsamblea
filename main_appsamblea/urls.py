from django.conf.urls import *
import views

from django.db.models.loading import cache as model_cache
if not model_cache.loaded:
    model_cache.get_models()

urlpatterns = patterns('',
                       (r'^$', views.main_page),
                       (r'registro', views.registro),
                       (r'crearAsamblea', views.crear_asamblea),
                       (r'test_facebook', views.facebook_test),
                       (r'eliminarAsamblea', views.eliminarAsamblea),
                       (r'obtenerAsambleas', views.obtenerAsambleas),
                       (r'obtenerAsamblea', views.obtenerAsamblea),
                       (r'inscribirseEnAsamblea', views.inscribirseEnAsamblea),
                       (r'abandonarAsamblea', views.abandonarAsamblea),
                       )
