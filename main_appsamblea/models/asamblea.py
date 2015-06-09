# -*- encoding: utf-8 -*-
from __future__ import division
import json
from django.core.validators import URLValidator
from google.appengine.ext import ndb
from main_appsamblea.models.usuario import Usuario


class Asamblea(ndb.Model):
    nombre = ndb.StringProperty()
    fecha = ndb.DateProperty()
    hora = ndb.TimeProperty()
    lugar = ndb.StringProperty()
    descripcion = ndb.StringProperty()
    es_abierta = ndb.BooleanProperty()
    url_streaming = ndb.StringProperty()
    url_asamblea = ndb.StringProperty()
    creador = ndb.KeyProperty(kind="Usuario")
    # TODO: descomentar cuando se implemente la organización
    # organizacion = ndb.KeyProperty(kind=Organizacion)

    @property
    def asistentes(self):
        return Usuario.query().filter(Usuario.asistente_asambleas == self.key)

    def add_asistente(self, usuario):
        usuario.asistente_asambleas.append(self.key)
        usuario.put()

    def eliminar_asistente(self, usuario):
        usuario.asistente_asambleas.remove(self.key)
        usuario.put()

    def isOk(self):
        ok = ""
        val = URLValidator()
        # El nombre no puede estar vacío. En python se puede comprobar pasando la cadena a booleano y viendo si está llena de caracteres vacíos
        if not bool(self.nombre) or self.nombre.isspace():
            ok += "El nombre está vacío\n"
        # La descripción no puede estar vacía
        if not bool(self.descripcion) or self.descripcion.isspace():
            ok += "La descripción debe de estar vacía\n"
        # Si existe la URL del streaming debe de estar funcionando
        if bool(self.url_streaming):
            try:
                val(self.url_streaming)
            except:
                ok += "La URL del streaming no funciona\n"
        # Si existe la URL de la asamblea debe de estar funcionando
        if bool(self.url_asamblea):
            try:
                val(self.url_asamblea)
            except:
                ok += "La URL de la asamblea no funciona\n"
        return ok

    def encode(self):
        return json.dumps({'id': self.key.id(), 'nombre': self.nombre, 'fecha': str(self.fecha),
                           'lugar': self.lugar, 'hora': str(self.hora),
                           'descripcion': self.descripcion, 'es_abierta': self.es_abierta,
                           'url_streaming': self.url_streaming, 'urlasamblea': self.url_asamblea,
                           'creador': self.creador.get().encode(),
                           # 'organizacion': self.organizacion.id
                           })  # Si para enviar. Para recibir es necsario introducirlo en la tabla participa, así que se debería hacer enviando esta.

    ''''@staticmethod
    def decode(obj):
        data = json.loads(obj)

        if data['model'] == 'Asamblea':
            n_id = data['pk']
            fields = data['fields']

            return Asamblea(id=n_id, nombre=fields['nombre'], fecha=fields['fecha'], lugar=fields['lugar'],
                            descripcion=fields['descripcion'], es_abierta=fields['es_abierta'],
                            url_streaming=fields['url_streaming'], urlasamblea=fields['urlasamblea'],
                            usuario_id=fields['usuario'], organizacion_id=fields['organizacion'])

        else:
            return None

    class Meta:
        app_label = 'main_appsamblea'''
