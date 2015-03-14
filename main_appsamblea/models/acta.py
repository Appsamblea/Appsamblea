# -*- encoding: utf-8 -*-

from __future__ import division
import json
from django.db import models
from main_appsamblea.models.asamblea import Asamblea

class Acta(models.Model):
	texto = models.TextField()
	asamblea = models.ForeignKey(Asamblea)

	def isOk(self):
		ok = ""

		#El texto no puede estar vacío
		if not bool (self.texto) or self.texto.isspace():
			ok += "El texto está vacío\n"

		return ok

	def encode(self):
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'texto': self.texto, 'asamblea': self.asamblea.id}})
		
	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Acta':
			n_id = data['pk']
			fields = data['fields']

			return Acta(id = n_id, texto = fields['texto'], asamblea_id = fields['asmablea'])
		else:
			return None

	class Meta:
		app_label = 'main_appsamblea'

