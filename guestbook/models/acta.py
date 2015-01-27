# -*- encoding: utf-8 -*-
'''
Created on 25/11/2014

@author: silt
'''
from __future__ import division
import datetime
import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models
from guestbook.models.asamblea import Asamblea

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
		return json.dumps({'texto': self.texto, \
							'asamblea': self.asamblea})
	
	def decode(obj):
		return json.loads(obj)	

	class Meta:
		app_label = 'guestbook'

