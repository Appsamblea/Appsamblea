# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import datetime
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
		return json.dumps('pk': self.id, 'model': self.__class__.__name__, 'fields':{'texto': self.texto, 'usuario_envia': self.usuario_envia.id, \
							'usuario_recibe': self.usuario_recibe.id, 'grupo': self.grupo.id})
	@staticmethod
	def decode(obj):
		data = json.loads(obj)
		if data['model'] == 'Mensaje':
			return Mensaje(id = data['pk'], texto = data['texto'], usuario_envia = ?, usuario_recibe = ?, grupo = ?)
			#Faltan usuario_envia, usuario_recibe y grupo.
		else:
			return None

	class Meta:
		app_label = 'guestbook'

