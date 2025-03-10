from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from area_geografica.models import Pais, Ciudad
from autenticacion.models import PerfilPersona
from landing.models import Conference, ConferenceFee, CommitteeCategory, TopicCategory, ScheduleConference

from pryiberoamericano import settings
from core.email_config import send_html_mail
from core.funciones import addData, mi_paginador, get_decrypt, get_client_ip
from core.notificacion_config import enviar_not_push
from public.models import VisitaEntorno
from seguridad.models import *
from django.utils.translation import gettext as _

def members(request):
    data = {
        'titulo': _('Members'),
        'ruta': request.path,
        'fecha': datetime.now(),
    }
    addData(request, data)
    confi_ = Configuracion.get_instancia()
    conference = Conference.objects.filter(status=True, active=True).order_by('-active', '-end_date').first()
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
        data['conference'] = conference
        committes = CommitteeCategory.objects.filter(status=True, active=True, conference=conference).order_by('order')
        data['committes'] = committes
        return render(request, 'public/landing/members.html', data)
