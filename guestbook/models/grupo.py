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
from guestbook.models.organizacion import Organizacion

class Grupo(models.Model):
	nombre = models.CharField(max_length = 256)
	descripcion = models.TextField()
	organizacion = models.ForeignKey(Organizacion)
	administrador = models.ForeignKey(Usuario, related_name = 'usuario_grupo_administrador')
	miembros = models.ManyToManyField(Usuario, related_name = 'usuario_grupo_miembros')

	def isOk(self):
		ok = ""
		if len(self.nombre) == 0 or self.nombre.isspace():
			ok+="El nombre del grupo no puede estar vacío\n"
		if len(self.descripcion) == 0 or self.descripcion.isspace():
			ok+="La descripción del grupo no puede estar vacío\n"
		return ok
		
	def encode(self):
		return json.dumps({'nombre': self.nombre, \
							'descripcion': self.descripcion, \
							'organizacion': self.organizacion, \
							'administrador': self.administrador, \
							'miembros': self.miembros})
	
	def decode(obj):
		return json.loads(obj)		

	class Meta:
		app_label = 'guestbook'

