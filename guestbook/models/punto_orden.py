# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import datetime
import json
from django.db import models
from guestbook.models.asamblea import Asamblea
from guestbook.models.turno_palabra import Turno_palabra

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
		if len(self.nombre) == 0 or self.nombre.isspace():
			ok+="El nombre del grupo no puede estar vacío\n"
		if len(self.descripcion) == 0 or self.descripcion.isspace():
			ok+="La descripción del grupo no puede estar vacío\n"
		return ok
		
	def encode(self):
		return json.dumps({'orden': self.orden, \
							'nombre': self.nombre, \
							'descripcion': self.descripcion, \
							'tratado': self.tratado, \
							'asamblea': self.asamblea, \
							'turnos_de_palabra': self.turnos_de_palabra})
	
	def decode(obj):
		return json.loads(obj)		

	class Meta:
		app_label = 'guestbook'

