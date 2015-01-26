# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import datetime
import json
from django.db import models
from guestbook.models.participa import Participa

class Votacion(models.Model):
	nombre = models.CharField(max_length = 256)
	tiempo_votacion = models.TimeField()
	participa = models.ForeignKey(Participa)

	def isOk(self):
		ok = ""

		#El nombre no puede estar vacío.
		if len(self.nombre) == 0 or self.nombre.isspace():
			ok += "El nombre no puede estar vacío\n"

		#El tiempo mínimo es un minuto.
		if (self.tiempo_votacion.hour * 60 + self.tiempo_votacion.minute + self.tiempo_votacion.second/60 + self.tiempo_votacion.microsecond/60000000) < 1:
			ok += "El tiempo mínimo es un minuto\n" 		
	
		return ok
		
	def encode(self):
		return json.dumps({'nombre': self.nombre, \
							'tiempo_votacion': self.tiempo_votacion, \
							'participa': self.participa})
	
	def decode(obj):
		return json.loads(obj)			

	class Meta:
		app_label = 'guestbook'

