# -*- encoding: utf-8 -*-
from __future__ import division
import json
from django.core.validators import URLValidator
from django.db import models
from guestbook.models.usuario import Usuario

class Organizacion(models.Model):
	nombre = models.CharField(max_length = 256)
	tematica = models.CharField(max_length = 256)
	logo = models.ImageField(max_length = 256*256, upload_to='imagenes')
	descripcion = models.TextField(null = True)
	facebook_id = models.IntegerField(unique = True, null = True)
	gplus_id = models.IntegerField(unique = True, null = True)
	email = models.EmailField(max_length = 256, null = True)
	web = models.URLField(null = True)
	miembros = models.ManyToManyField(Usuario, null = True)

	def isOk(self):				
		ok = ""
		val = URLValidator()
		#El nombre no puede estar vacío
		if not bool (self.nombre) or self.nombre.isspace():
			ok += "El nombre está vacío\n"
		#La temática no puede estar vacía
		if not bool (self.tematica) or self.tematica.isspace():
			ok += "La temática está vacía\n"
		#La descripción no puede estar vacía
		if not bool (self.descripcion) or self.descripcion.isspace():
			ok += "La descripción está vacía\n"
		#La web si está tiene que funcionar
		if bool (self.web):
			try:
				val(self.web)
			except:
				ok += "La URL de la organización no funciona\n"
		return ok
		
	def encode(self):
		if self.logo != "":
			url_logo = self.logo.url
		else:
			url_logo = ""

		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'nombre': self.nombre, \
							'tematica': self.tematica, \
							'logo': url_logo, \
							'descripcion': self.descripcion, \
							'facebook_id': self.facebook_id, \
							'email': self.email, \
							'gplus_id': self.gplus_id, \
							'web': self.web, \
							'miembros': [m.id for m in self.miembros.all()]}}) 

	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Organizacion':
			n_id = data['pk']
			fields = data['fields']

			o = Organizacion(id = n_id, tematica = fields['tematica'], logo = fields['logo'], descripcion = fields['descripcion'], facebook_id = fields['facebook_id'], email = fields['email'], gplus_id = fields['gplus_id'], web = fields['web'])

			o.miembros = fields['miembros']

			return o

		else:
			return None

	class Meta:
		app_label = 'guestbook'
