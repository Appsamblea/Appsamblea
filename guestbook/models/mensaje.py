# -*- encoding: utf-8 -*-
from __future__ import division
import json
from django.db import models
from guestbook.models.usuario import Usuario
from guestbook.models.grupo import Grupo

class Mensaje(models.Model):
	texto = models.TextField()
	usuario_envia = models.ForeignKey(Usuario, related_name = 'usuario_mensaje_envia')
	usuario_recibe = models.ForeignKey(Usuario, related_name = 'usuario_mensaje_recibe')
	grupo = models.ForeignKey(Grupo)

	def isOk(self):
		ok = ""

		#El texto no puede estar vacío.
		if len(self.texto) == 0 or self.texto.isspace():
			ok += "El texto no puede estar vacío\n"
	
		return ok
		
	def encode(self):
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields':{'texto': self.texto, 'usuario_envia': self.usuario_envia.id, \
							'usuario_recibe': self.usuario_recibe.id, 'grupo': self.grupo.id}})
	@staticmethod
	def decode(obj):
		data = json.loads(obj)
		
		if data['model'] == 'Mensaje':
			fields = data['fields']

			return Mensaje(id = data['pk'], texto = fields['texto'], usuario_envia_id = fields['usuario_envia'], usuario_recibe_id = fields['usuario_recibe'], grupo_id = fields['grupo'])

		else:
			return None

	class Meta:
		app_label = 'guestbook'

