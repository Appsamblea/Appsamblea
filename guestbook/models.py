# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
@author: potray
'''
from __future__ import division
import datetime
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models

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

class Usuario(models.Model):
	password = models.CharField(max_length = 256) #pass
	nombre = models.CharField(max_length = 256)
	apellidos = models.CharField(max_length = 256)
	fecha_nac = models.DateTimeField('fecha de nacimiento')
	telefono = models.CharField(max_length = 256)
	email = models.EmailField(max_length = 256)
	localidad = models.CharField(max_length = 256)
	pais = models.CharField(max_length = 256)
	bio = models.TextField()
	imagen_perfil = models.ImageField(max_length = 256*256, upload_to='imagenes')
	facebook_id = models.IntegerField(unique = True, null = True)
	twitter_id = models.IntegerField(unique = True, null = True)
	gplus_id = models.IntegerField(unique = True, null = True)
	puntos_exp = models.IntegerField(null = True)
	nivel = models.IntegerField(null = True)
	es_invitado = models.ManyToManyField('Participa', related_name = 'asamblea_participa', null = True)

	def isOk(self):
		ok = ""		
		if any(char.isdigit() for char in self.nombre):
			ok += "No se pueden incluir números en el nombre\n"
		if not any(char.isdigit() for char in self.telefono):
			ok += "Teléfono mal definido\n"
		if " " in self.email or "@" not in self.email or "." not in self.email:	
			ok+= "Email mal definido\n"		
		return ok
	
class Organizacion(models.Model):
	nombre = models.CharField(max_length = 256)
	tematica = models.CharField(max_length = 256)
	logo = models.ImageField(max_length = 256*256, upload_to='imagenes')
	descripcion = models.TextField(null = True)
	facebook_id = models.IntegerField(unique = True, null = True)
	gplus_id = models.IntegerField(unique = True, null = True)
	email = models.EmailField(max_length = 256, null = True)
	web = models.URLField(null = True)
	miembros = models.ManyToManyField(Usuario, null = True)

	def isOk(self):				
		ok = ""
		val = URLValidator()
		#El nombre no puede estar vacío
		if not bool (self.nombre) or self.nombre.isspace():
			ok += "El nombre está vacío\n"
		#La temática no puede estar vacía
		if not bool (self.tematica) or self.tematica.isspace():
			ok += "La temática está vacía\n"
		#La descripción no puede estar vacía
		if not bool (self.descripcion) or self.descripcion.isspace():
			ok += "La descripción está vacía\n"
		#La web si está tiene que funcionar
		if bool (self.web):
			try:
				val(self.web)
			except:
				ok += "La URL de la organización no funciona\n"
		return ok


class Asamblea(models.Model):
	nombre = models.CharField(max_length = 256)
	fecha = models.DateField()
	lugar = models.CharField(max_length = 256)
	descripcion = models.TextField()
	es_abierta = models.BooleanField(default = True)
	url_streaming = models.URLField(null = True)
	urlasamblea = models.URLField(null = True)
	usuario = models.ForeignKey(Usuario, related_name="asamblea_usuario")
	organizacion = models.ForeignKey(Organizacion)
	paricipantes = models.ManyToManyField(Usuario, through='Participa')

	def isOk(self):
		ok = ""
		val = URLValidator()
		#El nombre no puede estar vacío. En python se puede comprobar pasando la cadena a booleano y viendo si está llena de caracteres vacíos
		if not bool (self.nombre) or self.nombre.isspace():
			ok += "El nombre está vacío\n"
		#La descripción no puede estar vacía
		if not bool (self.descripcion) or self.descripcion.isspace():
			ok += "La descripción debe de estar vacía\n"
		#Si existe la URL del streaming debe de estar funcionando
		if bool (self.url_streaming):
			try:
				val(self.url_streaming)
			except:
				ok += "La URL del streaming no funciona\n"
		#Si existe la URL de la asamblea debe de estar funcionando
		if bool (self.urlasamblea):
			try:
				val(self.urlasamblea)
			except:
				ok += "La URL de la asamblea no funciona\n"
		return ok

class Acta(models.Model):
	texto = models.TextField()
	asamblea = models.ForeignKey(Asamblea)
	
class Documento(models.Model):
	nombre = models.CharField(max_length = 256)
	url = models.URLField()
	asamblea = models.ForeignKey(Asamblea)

	def isOk(self):
		ok = ""
		val = URLValidator()

		#El nombre no puede estar vacío.
		if len(self.nombre) == 0:
			ok += "El nombre no puede estar vacío\n"
	
		#Si existe la URL del documento debe de estar funcionando
		if bool (self.url):
			try:
				val(self.url)
			except:
				ok += "La URL del documento no funciona\n"

		return ok

class Grupo(models.Model):
	nombre = models.CharField(max_length = 256)
	descripcion = models.TextField()
	organizacion = models.ForeignKey(Organizacion)
	administrador = models.ForeignKey(Usuario, related_name = 'usuario_grupo_administrador')
	miembros = models.ManyToManyField(Usuario, related_name = 'usuario_grupo_miembros')
	def isOk(self):
		ok = ""
		if len(self.nombre) == 0:
			ok+="El nombre del grupo no puede estar vacío\n"
		if len(self.descripcion) == 0:
			ok+="La descripción del grupo no puede estar vacío\n"
		return ok

class Mensaje(models.Model):
	texto = models.TextField()
	usuario_envia = models.ForeignKey(Usuario, related_name = 'usuario_mensaje_envia')
	usuario_recibe = models.ForeignKey(Usuario, related_name = 'usuario_mensaje_recibe')
	grupo = models.ForeignKey(Grupo)

	def isOk(self):
		ok = ""

		#El texto no puede estar vacío.
		if len(self.texto) == 0:
			ok += "El texto no puede estar vacío\n"
	
		return ok

class Punto_orden_dia(models.Model):
	orden = models.IntegerField()
	nombre = models.CharField(max_length = 256)
	descripcion = models.TextField()
	tratado = models.BooleanField(default = False)
	asamblea = models.ForeignKey(Asamblea)
	turnos_de_palabra = models.ManyToManyField('Turno_palabra')
	def isOk(self):
		ok = ""
		if self.orden < 0:
			ok+="El orden del día no puede ser negativo\n"
		if len(self.nombre) == 0:
			ok+="El nombre del grupo no puede estar vacío\n"
		if len(self.descripcion) == 0:
			ok+="La descripción del grupo no puede estar vacío\n"
		return ok

class Participa(models.Model):
	usuario = models.ForeignKey(Usuario)
	asamblea = models.ForeignKey(Asamblea)
	unique_together = ("usuario", "asamblea")

class Turno_palabra(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.TextField()
	duracion = models.TimeField()
	duracion_estimada = models.TimeField()
	orden = models.IntegerField()
	realizado = models.BooleanField(default = False)
	participa = models.ForeignKey('Participa')
	unique_together = ("id", "participa")
	def isOk(self):
		ok = ""
		if len(self.descripcion) == 0:
			ok+="La descripción del turno de palabra no puede estar vacía\n"
		if self.orden < 0:
			ok+="El orden del turno de palabra no puede ser inferior a cero"
		if self.duracion < 0:
			ok+="La duración del turno de palabra no puede ser 0"
		if self.duracion_estimada < 0:
			ok+="La duración estimada del turno de palabra no puede ser 0"
		return ok

class Votacion(models.Model):
	nombre = models.CharField(max_length = 256)
	tiempo_votacion = models.TimeField()
	participa = models.ForeignKey(Participa)

	def isOk(self):
		ok = ""

		#El nombre no puede estar vacío.
		if len(self.nombre) == 0:
			ok += "El nombre no puede estar vacío\n"

		#El tiempo mínimo es un minuto.
		if (self.tiempo_votacion.hour * 60 + self.tiempo_votacion.minute + self.tiempo_votacion.second/60 + self.tiempo_votacion.microsecond/60000000) < 1:
			ok += "El tiempo mínimo es un minuto\n" 		
	
		return ok

class Votacion_opcion(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length = 256)
	votacion = models.ForeignKey(Votacion)
	participa = models.ManyToManyField(Participa)
	unique_together = ("id", "votacion")
	def isOk(self):
		ok = ""
		if len(self.nombre) == 0:
			ok+="La opción de la votación no puede estar vacía\n"
		return ok

class Responsabilidad(models.Model):
	nombre = models.CharField(max_length = 256)
	tipo = models.CharField(max_length = 256)
	asamblea_responsable = models.ManyToManyField(Asamblea)
	participante_realiza = models.ManyToManyField(Participa)

	def isOk(self):
		ok = ""

		#El nombre no puede estar vacío.
		if len(self.nombre) == 0:
			ok += "El nombre no puede estar vacío\n"

		#El tipo no puede estar vacío.
		if len(self.tipo) == 0:
			ok += "El tipo no puede estar vacío\n"
