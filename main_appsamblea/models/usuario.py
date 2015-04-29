# -*- encoding: utf-8 -*-
from __future__ import division
import json
from django.db import models


class Usuario(models.Model):
    password = models.CharField(max_length=256)  # pass
    nombre = models.CharField(max_length=256)
    apellidos = models.CharField(max_length=256)
    fecha_nac = models.DateTimeField('fecha de nacimiento')
    telefono = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    localidad = models.CharField(max_length=256)
    pais = models.CharField(max_length=256)
    bio = models.TextField()
    imagen_perfil = models.ImageField(max_length=256 * 256, upload_to='imagenes')
    facebook_id = models.IntegerField(unique=True, null=True)
    twitter_id = models.IntegerField(unique=True, null=True)
    gplus_id = models.IntegerField(unique=True, null=True)
    puntos_exp = models.IntegerField(null=True)
    nivel = models.IntegerField(null=True)
    es_invitado = models.ManyToManyField('Participa', related_name='asamblea_participa', null=True)

    def isOk(self):
        ok = ""
        # Contraseña no puede ser nula
        if not bool(self.password) or self.password.isspace():
            ok += "La contraseña no puede estar vacía\n"
        #Nombre no puede estar vacío
        if not bool(self.nombre) or self.nombre.isspace():
            ok += "El nombre no puede estar vacío\n"
        #Apellidos no puede estar vacío
        if not bool(self.apellidos) or self.nombre.isspace():
            ok += "Los apellidos no pueden estar vacíos\n"
        if any(char.isdigit() for char in self.nombre):
            ok += "No se pueden incluir números en el nombre\n"
        if any(not char.isdigit() for char in self.telefono):
            ok += "Teléfono mal definido\n"
        return ok

    def encode(self):
        return json.dumps({'nombre': self.nombre, \
                           'password': self.password, \
                           'apellidos': self.apellidos, \
                           'fecha_nac': self.fecha_nac, \
                           'telefono': self.telefono, \
                           'email': self.email, \
                           'localidad': self.localidad, \
                           'pais': self.pais, \
                           'bio': self.bio, \
                           'imagen_perfil': self.imagen_perfil, \
                           'facebook_id': self.facebook_id, \
                           'twitter_id': self.twitter_id, \
                           'gplus_id': self.gplus_id, \
                           'puntos_exp': self.puntos_exp, \
                           'nivel': self.nivel, \
                           'es_invitado': self.es_invitado})

    def decode(obj):
        return json.loads(obj)

    def encode(self):
        if self.imagen_perfil != "":
            url_imagen = self.imagen_perfil.url
        else:
            url_imagen = ""

        return json.dumps({'pk': self.id, 'model': self.__class__.__name__, 'fields': {'nombre': self.nombre, \
                                                                                       'password': self.password, \
                                                                                       'apellidos': self.apellidos, \
                                                                                       'fecha_nac': str(self.fecha_nac), \
                                                                                       'telefono': self.telefono, \
                                                                                       'email': self.email, \
                                                                                       'localidad': self.localidad, \
                                                                                       'pais': self.pais, \
                                                                                       'bio': self.bio, \
                                                                                       'imagen_perfil': url_imagen, \
                                                                                       'facebook_id': self.facebook_id, \
                                                                                       'twitter_id': self.twitter_id, \
                                                                                       'gplus_id': self.gplus_id, \
                                                                                       'puntos_exp': self.puntos_exp, \
                                                                                       'nivel': self.nivel, \
                                                                                       'es_invitado': [i.id for i in
                                                                                                       self.es_invitado.all()]}})  # Si para enviar. Para recibir es necsario introducirlo en la tabla participa, así que se debería hacer enviando esta.

    @staticmethod
    def decode(obj):
        data = json.loads(obj)

        if data['model'] == 'Usuario':
            n_id = data['pk']
            fields = data['fields']

            return Usuario(id=n_id, nombre=fields['nombre'], password=fields['password'], apellidos=fields['apellidos'],
                           fecha_nac=fields['fecha_nac'], telefono=fields['telefono'], email=fields['email'],
                           localidad=fields['localidad'], pais=fields['pais'], bio=fields['bio'],
                           imagen_perfil=fields['imagen_perfil'], facebook_id=fields['facebook_id'],
                           twitter_id=fields['twitter_id'], gplus_id=fields['gplus_id'],
                           puntos_exp=fields['puntos_exp'], nivel=fields['nivel'])

        else:
            return None

    class Meta:
        app_label = 'main_appsamblea'
