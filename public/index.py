from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from area_geografica.models import Pais, Ciudad
from autenticacion.models import PerfilPersona
from landing.models import Conference, ConferenceFee

from pryiberoamericano import settings
from core.email_config import send_html_mail
from core.funciones import addData, mi_paginador, get_decrypt, get_client_ip
from core.notificacion_config import enviar_not_push
from public.models import VisitaEntorno
from seguridad.models import *

def index(request):
    data = {
        'titulo': 'Home',
        'ruta': request.path,
        'fecha': datetime.now(),
    }
    addData(request, data)
    confi_ = Configuracion.get_instancia()

    if request.method == 'POST':
        res_json = []
        try:
            action = request.POST['action']
            if action == 'send_mail':
                nombre, email, telefono, mensaje = request.POST['name'], request.POST['email'], request.POST['phone'], \
                    request.POST['message']
                datos = {
                    'sucursal': request.config.nombre_empresa,
                    'nombres': nombre,
                    'correo': email,
                    'telefono': telefono,
                    'mensaje': mensaje
                }
                to = confi_.email_notificacion
                subject = f"New Message Received from the 'Contact Us' Landing Page"
                send_html_mail(subject, "email/email_contactanos.html", datos, [to], [], [])
                messages.success(request, 'Your message has been sent successfully.')
                res_json.append({'error': False, 'reload': True})

        except Exception as ex:
            res_json.append({'error': True, "message": f"Sorry, error occured this time sending your message. {ex}"})
        return JsonResponse(res_json, safe=False)
    elif request.method == 'GET':
        if 'action' in request.GET:
            data["action"] = action = request.GET['action']

        # CONTADOR ENTORNO
        ipresult = get_client_ip(request)
        dispositivo = request.META['HTTP_USER_AGENT']
        if not VisitaEntorno.objects.filter(fecha_visita=datetime.now().date(),
                                            ip=ipresult, dispositivo=dispositivo).exists():
            if not request.user.is_authenticated:
                VisitaEntorno.objects.create(fecha_visita=datetime.now().date(), ip=ipresult,
                                             hora_visita=datetime.now().time(),
                                             dispositivo=dispositivo)
            else:
                VisitaEntorno.objects.create(fecha_visita=datetime.now().date(), ip=ipresult,
                                             hora_visita=datetime.now().time(), user_id=request.user.pk,
                                             dispositivo=dispositivo)

        return render(request, 'public/landing/landing.html', data)
