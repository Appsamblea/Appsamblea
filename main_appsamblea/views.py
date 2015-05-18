# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from main_appsamblea.models import Usuario


def main_page(request):
    return render(request, 'main_appsamblea/main_page.html')


@csrf_exempt
def registro(request):

    respuesta = {}

    if request.method == 'POST':
        objetoJSON = json.loads(request.body, encoding='latin-1')
        print objetoJSON

        facebookID = objetoJSON['id']
        nombre = objetoJSON['nombre']
        apellidos = objetoJSON['apellidos']
        email = objetoJSON['email']


        nuevoUsuario = Usuario(username=facebookID, first_name=nombre, last_name=apellidos, email=email,
                               password=facebookID)

        isOk = nuevoUsuario.isOk()

        if isOk == "":
            nuevoUsuario.save()
            respuesta = 'ok'
        else:
            respuesta = isOk

    else:
        #Prueba del código anterior por GET
        facebookID = '845982745902730945234'
        nombre = 'Prueba'
        apellidos = 'Probando Probando'
        email = 'prueba@probando.com'


        nuevoUsuario = Usuario(username=facebookID, first_name=nombre, last_name=apellidos, email=email,
                               password=facebookID)

        isOk = nuevoUsuario.isOk()

        if isOk == "":
            nuevoUsuario.save()
            respuesta = 'ok'
        else:
            respuesta = isOk
        #respuesta = 'GET no permitido'

    return HttpResponse(
        json.dumps({'mensaje': respuesta})
    )


def facebook_test(request):
    return render(request, 'main_appsamblea/facebook_test.html')