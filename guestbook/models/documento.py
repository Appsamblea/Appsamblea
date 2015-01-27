# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''
from __future__ import division
import datetime
import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models
from guestbook.models.asamblea import Asamblea

class Documento(models.Model):
	nombre = models.CharField(max_length = 256)
	url = models.URLField()
	asamblea = models.ForeignKey(Asamblea)

	def isOk(self):
		ok = ""
		val = URLValidator()

		#El nombre no puede estar vacío.
		if len(self.nombre) == 0 or self.nombre.isspace():
			ok += "El nombre no puede estar vacío\n"
	
		#Si existe la URL del documento debe de estar funcionando
		if bool (self.url):
			try:
				val(self.url)
			except:
				ok += "La URL del documento no funciona\n"

		return ok
		
	def encode(self):
		return json.dumps('pk': self.id, 'model': self.__class__.__name__, 'fields':{'nombre': self.nombre, 'url': self.url, 'asamblea': self.asamblea.id})
		
	@staticmethod
	def decode(obj):
		data = json.loads(obj)
		if data['model'] == 'Documento':
			return Documento(id = data['pk'], nombre = data['nombre'], url = data['url'], asamblea = ?)
			#Falta asamblea
		else:
			return None

	class Meta:
		app_label = 'guestbook'
