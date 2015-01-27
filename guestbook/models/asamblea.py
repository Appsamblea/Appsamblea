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
from guestbook.models.usuario import Usuario
from guestbook.models.organizacion import Organizacion

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
		
	def encode(self):
		return json.dumps({'nombre': self.nombre, \
							'fecha': self.fecha, \
							'lugar': self.lugar, \
							'descripcion': self.descripcion, \
							'es_abierta': self.es_abierta, \
							'url_streaming': self.url_streaming, \
							'urlasamblea': self.urlasamblea, \
							'usuario': self.usuario, \
							'organizacion': self.organizacion, \
							'participantes': self.participantes})
	
	def decode(obj):
		return json.loads(obj)		

	class Meta:
		app_label = 'guestbook'
