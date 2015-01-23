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
from guestbook.models.usuario import Usuario

class Organizacion(models.Model):
	nombre = models.CharField(max_length = 256)
	tematica = models.CharField(max_length = 256)
	logo = models.ImageField(max_length = 256*256, upload_to='imagenes')
	descripcion = models.TextField(null = True)
	facebook_id = models.IntegerField(unique = True, null = True)
	gplus_id = models.IntegerField(unique = True, null = True)
	email = models.EmailField(max_length = 256, null = True)
	web = models.URLField(null = True)
	miembros = models.ManyToManyField(Usuario, null = True)

	def isOk(self):				
		ok = ""
		val = URLValidator()
		#El nombre no puede estar vacío
		if not bool (self.nombre) or self.nombre.isspace():
			ok += "El nombre está vacío\n"
		#La temática no puede estar vacía
		if not bool (self.tematica) or self.tematica.isspace():
			ok += "La temática está vacía\n"
		#La descripción no puede estar vacía
		if not bool (self.descripcion) or self.descripcion.isspace():
			ok += "La descripción está vacía\n"
		#La web si está tiene que funcionar
		if bool (self.web):
			try:
				val(self.web)
			except:
				ok += "La URL de la organización no funciona\n"
		return ok

	class Meta:
		app_label = 'guestbook'
