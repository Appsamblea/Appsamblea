from django.http import HttpResponse
from django.shortcuts import render


def main_page(request):
    return render(request, 'main_appsamblea/main_page.html')

def registro(request):
    if request.method == 'POST':
        return HttpResponse(
            request,
            'hola'
        )