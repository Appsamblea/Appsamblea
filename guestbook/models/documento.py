# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''
from __future__ import division
import datetime
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models
from guestbook.models.asamblea import Asamblea

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

	class Meta:
		app_label = 'guestbook'
