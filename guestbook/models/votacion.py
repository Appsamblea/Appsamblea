# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import datetime
import json
from django.db import models
from datetime import time
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
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'nombre': self.nombre, \
							'tiempo_votacion': self.tiempo_votacion.hour * 60 + self.tiempo_votacion.minute + self.tiempo_votacion.second/60 + self.tiempo_votacion.microsecond/60000000, \
							'participa': self.participa.id}})
	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Votacion':
			n_id = data['pk']
			fields = data['fields']
			n_nombre = fields['nombre']
			n_tiempo_total = fields['tiempo_votacion']
		
			n_tiempo_total_hour = int(n_tiempo_total//60)
			n_tiempo_total = n_tiempo_total - n_tiempo_total_hour*60
			n_tiempo_total_min = int(n_tiempo_total)
			n_tiempo_total = n_tiempo_total - n_tiempo_total_min
			n_tiempo_total = n_tiempo_total*60
			n_tiempo_total_sec = int(n_tiempo_total)
			n_tiempo_total_mic = int((n_tiempo_total - n_tiempo_total_sec)*1000000)
			n_tiempo_votacion = time(hour = n_tiempo_total_hour, minute = n_tiempo_total_min, second = n_tiempo_total_sec, microsecond = n_tiempo_total_mic)

			n_participa_id = fields['participa']

			return Votacion(id = n_id, nombre = n_nombre, tiempo_votacion = n_tiempo_votacion, participa_id = n_participa_id)

		else:
			return None

	class Meta:
		app_label = 'guestbook'

