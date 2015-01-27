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

	def encode(self):
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'usuario': self.usuario.id, \
							'asamblea': self.asamblea.id}})
	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Participa':
			n_id = data['pk']
			fields = data['fields']
			n_usuario_id = fields['usuario']
			n_asamblea_id = fields['asamblea']
		
			return Participa(id =  n_id, usuario_id = n_usuario_id, asamblea_id = n_asamblea_id)

		else:
			return None

	class Meta:
		unique_together = ("usuario", "asamblea")
		app_label = 'guestbook'
