# -*- encoding: utf-8 -*-
from __future__ import division
import json
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractUser
from google.appengine.ext import ndb
from django.db import models

#Propiedades en https://cloud.google.com/appengine/docs/python/ndb/properties
class Usuario(ndb.Model):

    id = ndb.IntegerProperty()
    password = ndb.StringProperty()
    nombre = ndb.StringProperty()
    apellidos = ndb.StringProperty()
    fecha_nac = ndb.DateProperty()
    telefono = ndb.IntegerProperty()
    email = ndb.StringProperty()
    localidad = ndb.StringProperty()
    pais = ndb.StringProperty()
    bio = ndb.StringProperty()
    #imagen_perfil = models.ImageField(max_length=256 * 256, upload_to='imagenes')
    facebook_id = ndb.IntegerProperty()
    twitter_id = ndb.IntegerProperty()
    gplus_id = ndb.IntegerProperty()
    puntos_exp = ndb.IntegerProperty()
    nivel = ndb.IntegerProperty()
    #es_invitado = models.ManyToManyField('Participa', related_name='asamblea_participa', null=True)

    def isOk(self):
        ok = ""
        # Contraseña no puede ser nula
        if not bool(self.password) or self.password.isspace():
            ok += "La contraseña no puede estar vacía\n"
        # Nombre no puede estar vacío
        if not bool(self.nombre) or self.nombre.isspace():
            ok += "El nombre no puede estar vacío\n"
        #Apellidos no puede estar vacío
        if not bool(self.apellidos) or self.apellidos.isspace():
            ok += "Los apellidos no pueden estar vacíos\n"
        if any(char.isdigit() for char in self.nombre):
            ok += "No se pueden incluir números en el nombre\n"
        return ok

    ''''def encode(self):
        return json.dumps({'username': self.username, 'nombre': self.first_name, 'password': self.password,
                           'last_name': self.last_name,
                           'fecha_nac': self.fecha_nac, 'telefono': self.telefono, 'email': self.email,
                           'localidad': self.localidad,
                           'pais': self.pais, 'bio': self.bio, 'imagen_perfil': self.imagen_perfil,
                           'facebook_id': self.facebook_id,
                           'twitter_id': self.twitter_id, 'gplus_id': self.gplus_id, 'puntos_exp': self.puntos_exp,
                           'nivel': self.nivel, 'es_invitado': self.es_invitado})

    def decode(obj):
        return json.loads(obj)

    def encode(self):
        if self.imagen_perfil != "":
            url_imagen = self.imagen_perfil.url
        else:
            url_imagen = ""

        return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'username': self.username,
                                                                                       'nombre': self.first_name,
                                                                                       'password': self.password,
                                                                                       'last_name': self.last_name,
                                                                                       'fecha_nac': str(self.fecha_nac),
                                                                                       'telefono': self.telefono,
                                                                                       'email': self.email,
                                                                                       'localidad': self.localidad,
                                                                                       'pais': self.pais,
                                                                                       'bio': self.bio,
                                                                                       'imagen_perfil': url_imagen,
                                                                                       'facebook_id': self.facebook_id,
                                                                                       'twitter_id': self.twitter_id,
                                                                                       'gplus_id': self.gplus_id,
                                                                                       'puntos_exp': self.puntos_exp,
                                                                                       'nivel': self.nivel,
                                                                                       'es_invitado': [i.id for i in
                                                                                                       self.es_invitado.all()]}})  # Si para enviar. Para recibir es necsario introducirlo en la tabla participa, así que se debería hacer enviando esta.

    @staticmethod
    def decode(obj):
        data = json.loads(obj)

        if data['model'] == 'Usuario':
            n_id = data['pk']
            fields = data['fields']

            return Usuario(id=n_id, nombre=fields['nombre'], password=fields['password'], last_name=fields['last_name'],
                           fecha_nac=fields['fecha_nac'], telefono=fields['telefono'], email=fields['email'],
                           localidad=fields['localidad'], pais=fields['pais'], bio=fields['bio'],
                           imagen_perfil=fields['imagen_perfil'],
                           facebook_id=fields['facebook_id'],
                           twitter_id=fields['twitter_id'], gplus_id=fields['gplus_id'],
                           puntos_exp=fields['puntos_exp'], nivel=fields['nivel'])

        else:
            return None'''''

#auth_models.User = Usuario