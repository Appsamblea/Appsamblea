'''
Created on 25/11/2014

@author: silt
'''
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    '''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
    '''Models an individual Guestbook entry.'''
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

def GetEntityViaMemcache(entity_key):
	'''Get entity from memcache if available, from datastore if not.'''
	entity = memcache.get(str(entity_key))

	if entity is not None:
		return entity
  
	entity = entity_key.get()
	
	if entity is not None:
		memcache.set(str(entity_key), entity)

	return entity

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Acta(models.Model):
    id = models.IntegerField(primary_key=True)
    texto = models.CharField(blank=True)
    id_asamblea = models.ForeignKey('Asamblea', db_column='id_asamblea')
    class Meta:
        db_table = 'acta'

class Asamblea(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True)
    fecha = models.DateField(null=True, blank=True)
    lugar = models.CharField(blank=True)
    descripcion = models.CharField(blank=True)
    es_abierta = models.IntegerField(null=True, blank=True)
    url_streaming = models.CharField(blank=True)
    url_asamblea = models.CharField(blank=True)
    id_usuario_crea = models.ForeignKey('Usuario', db_column='id_usuario_crea')
    id_organizacion_convoca = models.ForeignKey('Organizacion', db_column='id_organizacion_convoca')
    class Meta:
        db_table = 'asamblea'

class AsambleaTieneResponsabilidad(models.Model):
    id_asamblea = models.ForeignKey(Asamblea, db_column='id_asamblea')
    id_responsabilidad = models.ForeignKey('Responsabilidad', db_column='id_responsabilidad')
    class Meta:
        db_table = 'asamblea_tiene_responsabilidad'

class Documento(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255L)
    url = models.CharField(max_length=255L, blank=True)
    id_asamblea = models.ForeignKey(Asamblea, db_column='id_asamblea')
    class Meta:
        db_table = 'documento'

class Grupo(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255L, blank=True)
    descripcion = models.CharField(max_length=255L, blank=True)
    id_organizacion = models.ForeignKey('Organizacion', db_column='id_organizacion')
    id_usuario_administrador = models.ForeignKey('Usuario', db_column='id_usuario_administrador')
    class Meta:
        db_table = 'grupo'

class Invita(models.Model):
    usuario = models.ForeignKey('Participa', db_column='usuario')
    asamblea = models.ForeignKey('Participa', db_column='asamblea')
    usuario_invitado = models.IntegerField()
    class Meta:
        db_table = 'invita'

class Mensaje(models.Model):
    id = models.IntegerField(primary_key=True)
    texto = models.CharField(max_length=255L, blank=True)
    id_usuario_envia = models.ForeignKey('Usuario', db_column='id_usuario_envia')
    id_usuario_recibe = models.ForeignKey('Usuario', null=True, db_column='id_usuario_recibe', blank=True)
    id_grupo_recibe = models.ForeignKey(Grupo, null=True, db_column='id_grupo_recibe', blank=True)
    class Meta:
        db_table = 'mensaje'

class Organizacion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField()
    tematica = models.CharField(max_length=255L, blank=True)
    logo = models.CharField(blank=True)
    descripcion = models.CharField(blank=True)
    facebook_id = models.CharField(max_length=255L, blank=True)
    gplus_id = models.CharField(max_length=255L, blank=True)
    email = models.CharField(max_length=255L, blank=True)
    web = models.CharField(blank=True)
    class Meta:
        db_table = 'organizacion'

class Participa(models.Model):
    id_usuario = models.ForeignKey('Usuario', db_column='id_usuario')
    id_asamblea = models.ForeignKey(Asamblea, db_column='id_asamblea')
    class Meta:
        db_table = 'participa'

class PuntoOrdenDia(models.Model):
    id = models.IntegerField(primary_key=True)
    orden = models.IntegerField()
    nombre = models.CharField(max_length=255L)
    descripcion = models.CharField(blank=True)
    tratado = models.IntegerField(null=True, blank=True)
    id_asamblea = models.ForeignKey(Asamblea, db_column='id_asamblea')
    class Meta:
        db_table = 'punto_orden_dia'

class Responsabilidad(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255L, blank=True)
    tipo = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'responsabilidad'

class ResponsabilidadRealiza(models.Model):
    id_responsabilidad = models.ForeignKey(Responsabilidad, db_column='id_responsabilidad')
    id_usuario = models.ForeignKey(Participa, db_column='id_usuario')
    id_asamblea = models.ForeignKey(Participa, db_column='id_asamblea')
    class Meta:
        db_table = 'responsabilidad_realiza'

class TurnoPalabra(models.Model):
    id = models.IntegerField()
    descripcion = models.CharField()
    duracion = models.TextField(blank=True) # This field type is a guess.
    duracion_estimada = models.TextField(blank=True) # This field type is a guess.
    orden = models.IntegerField()
    realizado = models.IntegerField(null=True, blank=True)
    id_usuario = models.ForeignKey(Participa, db_column='id_usuario')
    id_asamblea = models.ForeignKey(Participa, db_column='id_asamblea')
    class Meta:
        db_table = 'turno_palabra'

class TurnoPalabraSobrePuntoOrdenDia(models.Model):
    id_turno_palabra = models.ForeignKey(TurnoPalabra, db_column='id_turno_palabra')
    id_punto_orden_dia = models.ForeignKey(PuntoOrdenDia, db_column='id_punto_orden_dia')
    class Meta:
        db_table = 'turno_palabra_sobre_punto_orden_dia'

class Usuario(models.Model):
    id = models.IntegerField(primary_key=True)
    pass_field = models.CharField(max_length=255L, db_column='pass') # Field renamed because it was a Python reserved word.
    nombre = models.CharField()
    apellidos = models.CharField(blank=True)
    fecha_nac = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=255L, blank=True)
    email = models.CharField()
    localidad = models.CharField(max_length=255L, blank=True)
    pais = models.CharField(max_length=255L, blank=True)
    bio = models.CharField(blank=True)
    imagen_perfil = models.CharField(blank=True)
    facebook_id = models.IntegerField(null=True, blank=True)
    twitter_id = models.IntegerField(null=True, blank=True)
    gplus_id = models.IntegerField(null=True, blank=True)
    puntos_exp = models.IntegerField()
    nivel = models.IntegerField()
    class Meta:
        db_table = 'usuario'

class UsuarioPerteneceGrupo(models.Model):
    id_usuario = models.ForeignKey(Usuario, db_column='id_usuario')
    id_grupo = models.ForeignKey(Grupo, db_column='id_grupo')
    class Meta:
        db_table = 'usuario_pertenece_grupo'

class UsuarioPerteneceOrganizacion(models.Model):
    id_usuario = models.ForeignKey(Usuario, db_column='id_usuario')
    id_organizacion = models.ForeignKey(Organizacion, db_column='id_organizacion')
    class Meta:
        db_table = 'usuario_pertenece_organizacion'

class Votacion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255L, blank=True)
    tiempo_votacion = models.DateTimeField(null=True, blank=True)
    id_usuario_crea = models.ForeignKey(Participa, db_column='id_usuario_crea')
    id_asamblea = models.ForeignKey(Participa, db_column='id_asamblea')
    class Meta:
        db_table = 'votacion'

class VotacionOpcion(models.Model):
    id_votacion = models.ForeignKey(Votacion, db_column='id_votacion')
    id = models.IntegerField()
    nombre = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'votacion_opcion'

class VotacionVoto(models.Model):
    id_usuario = models.ForeignKey(Participa, db_column='id_usuario')
    id_asamblea = models.ForeignKey(Participa, db_column='id_asamblea')
    id_votacion = models.ForeignKey(VotacionOpcion, db_column='id_votacion')
    id_opcion = models.ForeignKey(VotacionOpcion, db_column='id_opcion')
    class Meta:
        db_table = 'votacion_voto'

