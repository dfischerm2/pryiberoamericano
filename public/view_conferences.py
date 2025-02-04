from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from area_geografica.models import Pais, Ciudad
from autenticacion.models import PerfilPersona
from landing.models import Conference, ConferenceFee, CommitteeCategory, TopicCategory, ScheduleConference, \
    PhotoCatalogConference

from pryiberoamericano import settings
from core.email_config import send_html_mail
from core.funciones import addData, mi_paginador, get_decrypt, get_client_ip
from core.notificacion_config import enviar_not_push
from public.models import VisitaEntorno
from seguridad.models import *
from seguridad.templatetags.templatefunctions import encrypt


def conferences(request):
    data = {
        'titulo': 'Eventos Anteriores',
        'ruta': request.path,
        'fecha': datetime.now(),
    }
    addData(request, data)
    confi_ = Configuracion.get_instancia()
    conference = request.session['conference']
    if request.method == 'POST':
        res_json = []
        try:
            action = request.POST['action']
            pass

        except Exception as ex:
            res_json.append({'error': True, "message": f"Sorry, error occured this time sending your message. {ex}"})
        return JsonResponse(res_json, safe=False)
    elif request.method == 'GET':
        if 'action' in request.GET:
            data["action"] = action = request.GET['action']
            if action == 'catalog':
                id = int(encrypt(request.GET['id']))
                data['conference'] = conference = Conference.objects.get(pk=id)
                data['catalog'] = PhotoCatalogConference.objects.filter(conference=conference, public=True, status=True)
                data['conference_social_medias'] = RedesSociales.objects.filter(conference=conference, publicar=True, status=True)
                return render(request, 'public/landing/catalog.html', data)

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
        data['conferences'] = Conference.objects.filter(status=True, active=True).order_by('-id')

        return render(request, 'public/landing/conferences.html', data)
