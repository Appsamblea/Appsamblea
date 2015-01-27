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
			ok+="El orden del turno de palabra no puede ser inferior a cero"
		if self.duracion < 0:
			ok+="La duración del turno de palabra no puede ser 0"
		if self.duracion_estimada < 0:
			ok+="La duración estimada del turno de palabra no puede ser 0"
		return ok
		
	def encode(self):
		return json.dumps({'id': self.id, \
							'descripcion': self.descripcion, \
							'duracion': self.duracion, \
							'duracion_estimada': self.duracion_estimada, \
							'orden': self.orden, \
							'realizado': self.realizado, \
							'participa': self.participa})
	
	def decode(obj):
		return json.loads(obj)		

	class Meta:
		app_label = 'guestbook'
		unique_together = ("id", "participa")

