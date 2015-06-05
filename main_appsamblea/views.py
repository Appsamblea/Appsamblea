# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from main_appsamblea.models import Usuario, Asamblea

# Poner a true para hacer pruebas entrando en distintas URL.
debugPorGet = True


def main_page(request):
    return render(request, 'main_appsamblea/main_page.html')

def registrarPorFacebook(facebook_id, nombre, apellidos, email):
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
            return HttpResponse(
                json.dumps({'mensaje': 'creado', 'id': facebook_id})
            )
        else:
            respuesta = isOk
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

        # Mandar un mensaje que diga que el usuario existe
        return HttpResponse(
            json.dumps({'mensaje': 'existe', 'id': facebook_id})
        )


def crear_asamblea_bdd(nombre, fecha, lugar, descripcion, es_abierta, id_creador):
    # Buscar el creador
    query = Usuario.query(Usuario.id == id_creador)
    usuarioExistente = query.get()

    if usuarioExistente is not None:
        # Crear la asamblea
        nuevaAsamblea = Asamblea(nombre=nombre, fecha=fecha, lugar=lugar, descripcion=descripcion,
                                 es_abierta=es_abierta, creador=usuarioExistente.key)
        nuevaAsamblea.put()
        # Hacer que el creador asista a la asamblea
        nuevaAsamblea.add_asistente(usuarioExistente)
        nuevaAsamblea.put()

        return HttpResponse(
            json.dumps({'mensaje': 'ok'})
        )
    else:
        return HttpResponse(
            json.dumps({'mensaje': 'fallo'})
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


@csrf_exempt
def crear_asamblea(request):

    if request.method == 'POST':
        # Cargar datos JSON
        objetoJSON = json.loads(request.body, encoding='latin-1')

        nombre = objetoJSON['nombre']
        dia = int(objetoJSON['dia'])
        mes = int(objetoJSON['mes'])
        anio = int(objetoJSON['anio'])
        lugar = objetoJSON['lugar']
        descripcion = objetoJSON['descripcion']
        es_abierta = bool(objetoJSON['esAbierta'])
        id_creador = int(objetoJSON['idCreador'])

        fecha = datetime.date(dia, mes, anio)

        return crear_asamblea_bdd(nombre, fecha, lugar, descripcion, es_abierta, id_creador)

    elif debugPorGet:
        nombre = 'Asamblea de prueba'
        fecha = datetime.date(2025, 12, 25)
        lugar = 'Palacio de Congresos de Granada'
        descripcion = 'Es una asamblea de prueba simplemente'
        es_abierta = True
        id_creador = 84598274590

        return crear_asamblea_bdd(nombre, fecha, lugar, descripcion, es_abierta, id_creador)

    else:
        return HttpResponse(
            json.dumps({'mensaje': 'GET no permitido'})
        )

'''
    Se elimina una asamblea a partir de su ID. Únicamente puede eliminarla su creador
    Parámetros: idAsamblea, idUsuario
    Hay que comprobar que el usuario es quien ha creado la asamblea.
'''
@csrf_exempt
def eliminarAsamblea(request):
    if request.method == "POST":
        return 0
    return 0

'''
    Se obtiene un listado de asambleas en función a la búsqueda
    Parámetros: idUsuario, nombre de la asamblea o ninguno.
    - Próximas asambleas de un usuario
    - Lista total de asambleas
'''
@csrf_exempt
def obtenerAsambleas(request):
    if request.method == "POST":
        return 0
    return 0


'''
    Se obtiene el contenido de una Asamblea (usuarios invitados, lugar, etc)
    Parámetros: idAsamblea.
'''
@csrf_exempt
def obtenerAsamblea(request):
    if request.method == "POST":
        return 0
    return 0

'''
    Se añade un usuario a una asamblea como asistente
    Parámetros: idAsamblea, idUsuario
    En el supuesto de que el usuario ya esté inscrito en la asamblea, no ocurrirá nada (hay que comprobarlo).
'''
@csrf_exempt
def inscribirseEnAsamblea(request):
    if request.method == "POST":
        return 0
    return 0

'''
    Se elimina la asociación de un usuario con una asamblea
    Parámetros: idAsamblea, idUsuario
    En el supuesto de que el usuario que quiera abandonar la asamblea sea el creador de la misma, ésta se elimina.
'''
@csrf_exempt
def abandonarAsamblea(request):
    if request.method == "POST":
        return 0
    return 0


def facebook_test(request):
    return render(request, 'main_appsamblea/facebook_test.html')