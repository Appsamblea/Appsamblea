# -*- encoding: utf-8 -*-

from __future__ import division
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
			ok+="La descripción del grupo no puede estar vacía\n"

		return ok
		
	def encode(self):
		return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'nombre': self.nombre, \
							'descripcion': self.descripcion, \
							'organizacion': self.organizacion.id, \
							'administrador': self.administrador.id, \
							'miembros': [m.id for m in self.miembros.all()]}})

	@staticmethod
	def decode(obj):
		data = json.loads(obj)

		if data['model'] == 'Grupo':
			n_id = data['pk']
			fields = data['fields']
			g = Grupo(id = n_id, nombre = fields['nombre'], descripcion = fields['descripcion'], organizacion_id = fields['organizacion'], administrador_id = fields['administrador'])
			g.miembros = fields['miembros']

			return g

		else:
			return None

	class Meta:
		app_label = 'guestbook'

