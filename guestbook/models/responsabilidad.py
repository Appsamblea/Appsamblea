# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import json
from django.db import models
from guestbook.models.participa import Participa
from guestbook.models.asamblea import Asamblea

class Responsabilidad(models.Model):
	nombre = models.CharField(max_length = 256)
	tipo = models.CharField(max_length = 256)
	asamblea_responsable = models.ManyToManyField(Asamblea)
	participante_realiza = models.ManyToManyField(Participa)

	def isOk(self):
		ok = ""

		#El nombre no puede estar vacío.
		if len(self.nombre) == 0 or self.nombre.isspace():
			ok += "El nombre no puede estar vacío\n"

		#El tipo no puede estar vacío.
		if len(self.tipo) == 0 or self.tipo.isspace():
			ok += "El tipo no puede estar vacío\n"

		return ok
			
	def encode(self):
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'nombre': self.nombre, \
							'tipo': self.tipo, \
							'asamblea_responsable': [a.id for a in self.asamblea_responsable.all()], \
							'participante_realiza': [p.id for p in self.participante_realiza.all()]}})

	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Responsabilidad':
			n_id = data['pk']
			fields = data['fields']
			r = Responsabilidad(id = n_id, nombre = fields['nombre'], tipo = fields['tipo'])
			r.asamblea_responsable = fields['asamblea_responsable']
			r.participante_realiza = fields['participante_realiza']

			return r

		else:
			return None

	class Meta:
		app_label = 'guestbook'

