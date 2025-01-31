import json
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from autenticacion.models import Usuario, PerfilPersona
from core.custom_models import FormError
from core.email_config import send_html_mail
from core.funciones import addData, paginador, secure_module, log, generar_nombre
from django.contrib import messages

from landing.forms import ConferenceForm
from landing.models import Conference, ConferenceFee, TopicCategory
from pedidos.models import Pedido
from pryiberoamericano.settings import ID_GRUPO_USUARIO
from public.forms import RegisterUserForm, StudentAttendeeForm
from seguridad.templatetags.templatefunctions import encrypt


def registerView(request):
    data = {
        'titulo': 'Registro',
        'modulo': 'Landing',
        'ruta': request.path,
        'fecha': str(date.today())
    }
    addData(request, data)
    if request.method == 'POST':
        res_json = []
        try:
            pass

        except ValueError as ex:
            res_json.append({'error': True, "message": str(ex)})
        except FormError as ex:
            res_json.append(ex.dict_error)
        except Exception as ex:
            res_json.append({'error': True, "message": f"{ex}"})
        return JsonResponse(res_json, safe=False)
    elif request.method == 'GET':
        if 'action' in request.GET:
            data["action"] = action = request.GET['action']
            pass

        pass
