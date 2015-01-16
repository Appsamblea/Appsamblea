'''
Created on 25/11/2014

@author: silt
@author: potray
'''
import datetime
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users
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
	imagen_perfil = models.ImageField(max_length = 256*256)
	facebook_id = models.IntegerField(unique = True)
	twitter_id = models.IntegerField(unique = True)
	gplus_id = models.IntegerField(unique = True)
	puntos_exp = models.IntegerField()
	nivel = models.IntegerField()
	es_invitado = models.ManyToManyField('Participa')

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
	logo = models.ImageField(max_length = 256*256)
	description = models.TextField()
	facebook_id = models.IntegerField(unique = True)
	gplus_id = models.IntegerField(unique = True)
	email = models.EmailField(max_length = 256)
	web = models.URLField()
	miembros = models.ManyToManyField(Usuario)

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
	lugar = models.CharField()
	descripcion = models.TextField()
	es_abierta = models.BooleanField()
	url_streaming = models.URLField()
	urlasamblea = models.URLField()
	usuario = models.ForeignKey(Usuario)
	organizacion = models.ForeignKey(Organizacion)
	paricipantes = models.ManyToManyField(Usuario, through='Participa')

	def isOk(self):
		ok = true
		#nombre
		if self.nombre == "" or self.nombre == " ":
			ok = false
		#fecha
		
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
	administrador = models.ForeignKey(Usuario)
	miembros = models.ManyToManyField(Usuario)

class Mensaje(models.Model):
	texto = models.TextField()
	usuario_envia = models.ForeignKey(Usuario)
	usuario_recibe = models.ForeignKey(Usuario)
	grupo = models.ForeignKey(Grupo)

class Punto_orden_dia(models.Model):
	orden = models.IntegerField()
	nombre = models.CharField(max_length = 256)
	descripcion = models.TextField()
	tratado = models.BooleanField()
	asamblea = models.ForeignKey(Asamblea)
	turnos_de_palabra = models.ManyToManyField('Turno_palabra')

class Turno_palabra(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.TextField()
	duracion = models.TimeField()
	duracion_estimada = models.TimeField()
	orden = models.IntegerField()
	realizado = models.BooleanField()
	participa = models.ForeignKey('Participa', primary_key=True)
	
class Participa(models.Model):
	usuario = models.ForeignKey(Usuario, primary_key=True)
	asamblea = models.ForeignKey(Asamblea, primary_key=True)

class Votacion(models.Model):
	nombre = models.CharField(max_length = 256)
	tiempo_votacion = models.DateTimeField(auto_now_add=True)
	participa = models.ForeignKey(Participa)

class Votacion_opcion(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length = 256)
	votacion = models.ForeignKey(Votacion, primary_key=True)
	participa = models.ManyToManyField(Participa)

class Responsabilidad(models.Model):
	nombre = models.CharField(max_length = 256)
	tipo = models.CharField(max_length = 256)
	asamblea_responsable = models.ManyToManyField(Asamblea)
	participante_realiza = models.ManyToManyField(Participa)
