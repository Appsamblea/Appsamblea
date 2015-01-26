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
		return json.dumps({'texto': self.texto, \
							'usuario_envia': self.usuario_envia, \
							'usuario_recibe': self.usuario_recibe, \
							'grupo': self.grupo})
	
	def decode(obj):
		return json.loads(obj)			

	class Meta:
		app_label = 'guestbook'

