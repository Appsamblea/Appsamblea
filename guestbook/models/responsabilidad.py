# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import datetime
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

	class Meta:
		app_label = 'guestbook'

