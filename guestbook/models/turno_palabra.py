# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import json
from django.db import models
from datetime import time

class Turno_palabra(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.TextField()
	duracion = models.TimeField()
	duracion_estimada = models.TimeField()
	orden = models.IntegerField()
	realizado = models.BooleanField(default = False)
	participa = models.ForeignKey('Participa')
	
	def isOk(self):
		ok = ""
		if len(self.descripcion) == 0 or self.descripcion.isspace():
			ok+="La descripción del turno de palabra no puede estar vacía\n"
		if self.orden < 0:
			ok+="El orden del turno de palabra no puede ser inferior a cero\n"
		#Duración y duración estimada son campos de tiempo por lo que no es necesario hacer tests.
		return ok
		
	def encode(self):
		return json.dumps({'id': self.id, \
							'descripcion': self.descripcion, \
							'duracion': self.duracion.hour * 60 + self.duracion.minute + self.duracion.second/60 + self.duracion.microsecond/60000000, \
							'duracion_estimada': self.duracion_estimada.hour * 60 + self.duracion_estimada.minute + self.duracion_estimada.second/60 + self.duracion_estimada.microsecond/60000000, \
							'orden': self.orden, \
							'realizado': str(self.realizado), \
							'participa': self.participa.id})
	
	def decode(obj):
		return json.loads(obj)		

	def encode(self):
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'descripcion': self.descripcion, \
							'duracion': self.duracion.hour * 60 + self.duracion.minute + self.duracion.second/60 + self.duracion.microsecond/60000000, \
							'duracion_estimada': self.duracion_estimada.hour * 60 + self.duracion_estimada.minute + self.duracion_estimada.second/60 + self.duracion_estimada.microsecond/60000000, \
							'orden': self.orden, \
							'realizado': str(self.realizado), \
							'participa': self.participa.id}})
	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Turno_palabra':
			n_id = data['pk']
			fields = data['fields']
			n_duracion_total = fields['duracion']
		
			n_duracion_total_hour = int(n_duracion_total//60)
			n_duracion_total = n_duracion_total - n_duracion_total_hour*60
			n_duracion_total_min = int(n_duracion_total)
			n_duracion_total = n_duracion_total - n_duracion_total_min
			n_duracion_total = n_duracion_total*60
			n_duracion_total_sec = int(n_duracion_total)
			n_duracion_total_mic = int((n_duracion_total - n_duracion_total_sec)*1000000)
			n_duracion = time(hour = n_duracion_total_hour, minute = n_duracion_total_min, second = n_duracion_total_sec, microsecond = n_duracion_total_mic)

			n_duracion_estimada_total = fields['duracion_estimada']
		
			n_duracion_estimada_total_hour = int(n_duracion_estimada_total//60)
			n_duracion_estimada_total = n_duracion_estimada_total - n_duracion_estimada_total_hour*60
			n_duracion_estimada_total_min = int(n_duracion_estimada_total)
			n_duracion_estimada_total = n_duracion_estimada_total - n_duracion_estimada_total_min
			n_duracion_estimada_total = n_duracion_estimada_total*60
			n_duracion_estimada_total_sec = int(n_duracion_estimada_total)
			n_duracion_estimada_total_mic = int((n_duracion_estimada_total - n_duracion_estimada_total_sec)*1000000)
			n_duracion_estimada = time(hour = n_duracion_estimada_total_hour, minute = n_duracion_estimada_total_min, second = n_duracion_estimada_total_sec, microsecond = n_duracion_estimada_total_mic)

			return Turno_palabra(id = n_id, descripcion = fields['descripcion'], duracion = n_duracion, duracion_estimada = n_duracion_estimada, orden = fields['orden'], realizado = fields['realizado'], participa_id = fields['participa'])

		else:
			return None

	class Meta:
		app_label = 'guestbook'
		unique_together = ("id", "participa")

