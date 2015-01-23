# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''

from __future__ import division
import datetime
from django.db import models
from guestbook.models.participa import Participa
from guestbook.models.votacion import Votacion

class Votacion_opcion(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length = 256)
	votacion = models.ForeignKey(Votacion)
	participa = models.ManyToManyField(Participa)
	unique_together = ("id", "votacion")

	def isOk(self):
		ok = ""
		if len(self.nombre) == 0 or self.nombre.isspace():
			ok+="La opción de la votación no puede estar vacía\n"
		return ok

	class Meta:
		app_label = 'guestbook'

