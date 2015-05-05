from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def main_page(request):
    return render(request, 'main_appsamblea/main_page.html')

@csrf_exempt
def registro(request):
    if request.method == 'POST':
        return HttpResponse(
            request,
            'hola'
        )
    else:
        return render(request, 'main_appsamblea/main_page.html')