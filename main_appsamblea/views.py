# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from main_appsamblea.models import Usuario

debugPorGet = True


def main_page(request):
    return render(request, 'main_appsamblea/main_page.html')


def registrarPorFacebook (facebook_id, nombre, apellidos, email):
    # Ver si existe un usuario con el mismo ID de Facebook
    query = Usuario.query(Usuario.id == facebook_id)
    usuarioExistente = query.get()
    if usuarioExistente is None:
        # No existe, crearlo
        nuevoUsuario = Usuario(id=facebook_id, nombre=nombre, apellidos=apellidos, email=email,
                               password=str(facebook_id), facebook_id=facebook_id)

        # Comprobar integridad
        isOk = nuevoUsuario.isOk()

        if isOk == "":
            nuevoUsuario.put()
            respuesta = 'creado'
        else:
            respuesta = isOk

        # Mandar respuesta
        return HttpResponse(
            json.dumps({'mensaje': respuesta})
        )
    else:
        # Comprobación de integridad. El usuario existe, comprobar si dicho usuario tiene facebookID
        query = Usuario.query(Usuario.id == facebook_id)
        usuarioExistente = query.get()
        print usuarioExistente
        idFacebookExistente = usuarioExistente.facebook_id

        if idFacebookExistente == None:
            # Cambiársela
            usuarioExistente.facebook_id = facebook_id
            usuarioExistente.put()

        #Mandar un mensaje que diga que el usuario existe
        return HttpResponse(
            json.dumps({'mensaje': 'existe'})
        )

@csrf_exempt
def registro(request):

    respuesta = ''

    if request.method == 'POST':
        # Cargar datos JSON
        objetoJSON = json.loads(request.body, encoding='latin-1')

        facebookID = int(objetoJSON['id'])
        nombre = objetoJSON['nombre']
        apellidos = objetoJSON['apellidos']
        email = objetoJSON['email']

        return registrarPorFacebook(facebookID, nombre, apellidos, email)

    elif debugPorGet:
        # Prueba del código anterior por GET
        facebookID = 84598274590
        nombre = 'Prueba'
        apellidos = 'Probando Probando'
        email = 'prueba@probando.com'

        return registrarPorFacebook(facebookID, nombre, apellidos, email)

    else:
        return HttpResponse(
            json.dumps({'mensaje': 'GET no permitido'})
        )

def facebook_test(request):
    return render(request, 'main_appsamblea/facebook_test.html')