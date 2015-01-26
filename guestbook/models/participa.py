from __future__ import division
import datetime
import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models
from guestbook.models.usuario import Usuario
from guestbook.models.asamblea import Asamblea

class Participa(models.Model):
	usuario = models.ForeignKey(Usuario)
	asamblea = models.ForeignKey(Asamblea)
	unique_together = ("usuario", "asamblea")

	def encode(self):
		return json.dumps({'usuario': self.usuario, \
							'asamblea': self.asamblea})
	
	def decode(obj):
		return json.loads(obj)	
		
	class Meta:
		app_label = 'guestbook'
