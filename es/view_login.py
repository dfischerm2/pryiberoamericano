import base64
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.funciones import addData, ip_client_address, get_decrypt, datetime
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import activate

from landing.models import Conference
from pryiberoamericano import settings
from pryiberoamericano.settings import EMAIL_HOST_USER, URL_GENERAL
from autenticacion.models import Usuario

activate(settings.TIME_ZONE)


def login_tienda(request):
    data = {'titulo': 'Iniciar Sesión', 'url_auth':True}
    addData(request, data)
    if request.method == 'GET':
        des, data['next'] = get_decrypt(request.GET.get('next'))
        if not des:
            data['next'] = request.GET.get('next')
        if request.user.username != "":
            return redirect('/es/')
        return render(request, 'public/ES/seguridad/login.html', data)
    datos = {'resp': False}
    try:
        addData(request, data)
        if request.method == 'POST':
            usuario_, password = request.POST['usuario'], request.POST['password']
            if Usuario.objects.filter(username=usuario_).exists():
                user = authenticate(username=usuario_, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        if user.get_perfil_adm():
                            request.session['listConferences'] = listConferences = Conference.objects.filter(status=True).order_by('-active', '-end_date')
                            if listConferences:
                                conferences_actives = listConferences.filter(active=True).order_by('-id')
                                request.session['conference'] = conferences_actives.first() if conferences_actives else listConferences.first()
                        datos['resp'] = True
                        if request.POST.get('next'):
                            datos['redirect'] = request.POST.get('next')
                    else:
                        datos['error'] = 'Este usuario ha sido eliminado del sistema.'
                else:
                    datos['error'] = 'Credenciales Incorrectas'
            else:
                datos['error'] = 'No existe usuario.'
            return JsonResponse(datos)
    except Exception as ex:
        datos['error'] = 'Credenciales incorrectas'
        messages.error(request, ex)
        return JsonResponse(datos)


def logout_tienda(request):
    logout(request)
    return redirect('/es/')
