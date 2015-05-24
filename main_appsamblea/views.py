# -*- encoding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
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
    try:
        usuarioExistente = Usuario.objects.get(username=facebook_id)
    except ObjectDoesNotExist:
        # No existe, crearlo
        nuevoUsuario = Usuario(username=facebook_id, first_name=nombre, last_name=apellidos, email=email,
                               password=facebook_id, facebook_id=facebook_id)

        # Comprobar integridad
        isOk = nuevoUsuario.isOk()

        if isOk == "":
            nuevoUsuario.save()
            respuesta = 'creado'
        else:
            respuesta = isOk

        # Mandar respuesta
        return HttpResponse(
            json.dumps({'mensaje': respuesta})
        )
    else:
        # Comprobación de integridad. El usuario existe, comprobar si dicho usuario tiene facebookID
        usuarioExistente = Usuario.objects.get(username=facebook_id)
        idFacebookExistente = usuarioExistente.facebook_id

        if idFacebookExistente == None:
            # Cambiársela
            usuarioExistente.facebook_id = facebook_id
            usuarioExistente.save()

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

        facebookID = objetoJSON['id']
        nombre = objetoJSON['nombre']
        apellidos = objetoJSON['apellidos']
        email = objetoJSON['email']

        return registrarPorFacebook(facebookID, nombre, apellidos, email)

    elif debugPorGet:
        # Prueba del código anterior por GET
        facebookID = '84598274590'
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