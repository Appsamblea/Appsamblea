# -*- encoding: utf-8 -*-
from __future__ import division
import json
from django.db import models
from guestbook.models.participa import Participa
from guestbook.models.votacion import Votacion

class Votacion_opcion(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length = 256)
	votacion = models.ForeignKey(Votacion)
	participa = models.ManyToManyField(Participa)

	def isOk(self):
		ok = ""
		if len(self.nombre) == 0 or self.nombre.isspace():
			ok += "La opción de la votación no puede estar vacía\n"
		return ok
		
	def encode(self):
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'nombre': self.nombre, \
							'votacion': self.votacion.id, \
							'participa': [p.id for p in self.participa.all()]}})

	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Votacion_opcion':
			n_id = data['pk']
			fields = data['fields']

			v = Votacion_opcion(id = n_id, nombre = fields['nombre'], votacion_id = fields['votacion'])
			v.participa = fields['participa']			

			return v

		else:
			return None

	class Meta:
		app_label = 'guestbook'
		unique_together = ("id", "votacion")

