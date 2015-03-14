# -*- encoding: utf-8 -*-

from __future__ import division
import json
from django.core.validators import URLValidator
from django.db import models
from main_appsamblea.models.asamblea import Asamblea

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
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields':{'nombre': self.nombre, 'url': self.url, 'asamblea': self.asamblea.id}})
		
	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Documento':
			fields = data['fields']

			return Documento(id = data['pk'], nombre = fields['nombre'], url = fields['url'], asamblea_id = fields['asamblea'])
		else:
			return None

	class Meta:
		app_label = 'main_appsamblea'
