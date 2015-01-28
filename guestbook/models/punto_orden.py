# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import json
from django.db import models
from guestbook.models.asamblea import Asamblea

class Punto_orden_dia(models.Model):
	orden = models.IntegerField()
	nombre = models.CharField(max_length = 256)
	descripcion = models.TextField(null = False)
	tratado = models.BooleanField(default = False)
	asamblea = models.ForeignKey(Asamblea)
	turnos_de_palabra = models.ManyToManyField('Turno_palabra')

	def isOk(self):
		ok = ""
		if self.orden < 0:
			ok+="El orden del día no puede ser negativo\n"
		if len(self.nombre) == 0 or self.nombre.isspace():
			ok+="El nombre no puede estar vacío\n"
		if len(self.descripcion) == 0 or self.descripcion.isspace():
			ok+="La descripción no puede estar vacía\n"
		return ok
		
	def encode(self):
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'orden': self.orden, \
							'nombre': self.nombre, \
							'descripcion': self.descripcion, \
							'tratado': str(self.tratado), \
							'asamblea': self.asamblea.id, \
							'turnos_de_palabra': [t.id for t in self.turnos_de_palabra.all()]}}) #Si para enviar. Para recibir es necsario introducirlo en la tabla turno_palabra, así que se debería hacer enviando esta.
	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Punto_orden_dia':
			n_id = data['pk']
			fields = data['fields']

			return Punto_orden_dia(id = n_id, orden = fields['orden'], nombre = fields['nombre'], descripcion = fields['descripcion'], tratado = fields['tratado'], asamblea_id = fields['asamblea'])

		else:
			return None

	class Meta:
		app_label = 'guestbook'

