# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
@author: potray
'''
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

	def isOk(self):										#TEST USUARIO
							
		if any(char.isdigit() for char in self.nombre) \
			or not any(char.isdigit() for char in self.telefono) \
			or " " in self.email\
			or "@" not in self.email\
			or "." not in self.email:			
			return false
		else:
			return true								#FIN TEST USUARIO
	
class Organizacion(models.Model):
	nombre = models.CharField(max_length = 256)
	tematica = models.CharField(max_length = 256)
	logo = models.ImageField(max_length = 256*256, upload_to='imagenes')
	description = models.TextField(null = True)
	facebook_id = models.IntegerField(unique = True, null = True)
	gplus_id = models.IntegerField(unique = True, null = True)
	email = models.EmailField(max_length = 256, null = True)
	web = models.URLField(null = True)
	miembros = models.ManyToManyField(Usuario, null = True)

	def isOk(self):				
		if	" " in self.email\
			or "@" not in self.email\
			or "." not in self.email\
			or " " in self.web\
			or "." not in self.web:			
			return false
		else:
			return true

class Asamblea(models.Model):
	nombre = models.CharField(max_length = 256)
	fecha = models.DateTimeField()
	lugar = models.CharField(max_length = 256)
	descripcion = models.TextField()
	es_abierta = models.BooleanField()
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
		#La fecha tiene que ser una correcta. Tiene que estar en formato YYYY-mm-dd. En teoría por ser DateTimeField no te tiene que dejar meter otra cosa y habrá que hacer un parser.
		try:	
			datetime.datetime.strptime(self.fecha, '%Y-%m-%d')
			#El propio DateTimeField va a dar una excepción si intentamos poner una fecha del tipo 30 de Febrero por lo que no nos preocupamos de validarlo ahora.
		except:
			ok += "La fecha " + self.fecha + " debe de tener formato yyyy-mm-dd\n"
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

class Grupo(models.Model):
	nombre = models.CharField(max_length = 256)
	descripcion = models.TextField()
	organizacion = models.ForeignKey(Organizacion)
	administrador = models.ForeignKey(Usuario, related_name = 'usuario_grupo_administrador')
	miembros = models.ManyToManyField(Usuario, related_name = 'usuario_grupo_miembros')

class Mensaje(models.Model):
	texto = models.TextField()
	usuario_envia = models.ForeignKey(Usuario, related_name = 'usuario_mensaje_envia')
	usuario_recibe = models.ForeignKey(Usuario, related_name = 'usuario_mensaje_recibe')
	grupo = models.ForeignKey(Grupo)

class Punto_orden_dia(models.Model):
	orden = models.IntegerField()
	nombre = models.CharField(max_length = 256)
	descripcion = models.TextField()
	tratado = models.BooleanField()
	asamblea = models.ForeignKey(Asamblea)
	turnos_de_palabra = models.ManyToManyField('Turno_palabra')

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
	realizado = models.BooleanField()
	participa = models.ForeignKey('Participa')
	unique_together = ("id", "participa")

class Votacion(models.Model):
	nombre = models.CharField(max_length = 256)
	tiempo_votacion = models.DateTimeField(auto_now_add=True)
	participa = models.ForeignKey(Participa)

class Votacion_opcion(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length = 256)
	votacion = models.ForeignKey(Votacion)
	participa = models.ManyToManyField(Participa)
	unique_together = ("id", "votacion")

class Responsabilidad(models.Model):
	nombre = models.CharField(max_length = 256)
	tipo = models.CharField(max_length = 256)
	asamblea_responsable = models.ManyToManyField(Asamblea)
	participante_realiza = models.ManyToManyField(Participa)