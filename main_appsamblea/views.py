from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from main_appsamblea.models import Usuario


def main_page(request):
    return render(request, 'main_appsamblea/main_page.html')


@csrf_exempt
def registro(request):
    '''
    if request.method == 'POST':
        objetoJSON = json.loads(request.body)
        facebookID = objetoJSON['id']
        nombre = objetoJSON['nombre']
        apellidos = objetoJSON['apellidos']
        email = objetoJSON['email']

        nuevoUsuario = Usuario(username=facebookID, first_name=nombre, last_name=apellidos, email=email,
                               password=facebookID)
        if nuevoUsuario.isOk():
            nuevoUsuario.save()
            mensaje = 'ok'
        else:
            mensaje = 'error'

        return HttpResponse(
            mensaje
        )
    else:
        return render(request, 'main_appsamblea/main_page.html')
    '''
    return 'Registro'

def facebook_test(request):
    return render(request, 'main_appsamblea/facebook_test.html')