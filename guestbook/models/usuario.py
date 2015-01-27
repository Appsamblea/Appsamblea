# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''
from __future__ import division
from django.utils import timezone
import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models

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
		
	def encode(self):
		return json.dumps({'nombre': self.nombre, \
							'password': self.password, \
							'apellidos': self.apellidos, \
							'fecha_nac': self.fecha_nac, \
							'telefono': self.telefono, \
							'email': self.email, \
							'localidad': self.localidad, \
							'pais': self.pais, \
							'bio': self.bio, \
							'imagen_perfil': self.imagen_perfil, \
							'facebook_id': self.facebook_id, \
							'twitter_id': self.twitter_id, \
							'gplus_id': self.gplus_id, \
							'puntos_exp': self.puntos_exp, \
							'nivel': self.nivel, \
							'es_invitado': self.es_invitado})
	
	def decode(obj):
		return json.loads(obj)		

	class Meta:
		app_label = 'guestbook'
