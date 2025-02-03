from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import get_template
from landing.models import ScheduleConference, DetailScheduleConference
from landing.forms import ScheduleConferenceForm, DetailScheduleConferenceForm
from core.funciones_adicionales import salva_logs
from core.custom_forms import FormError
from core.funciones import secure_module, log, paginador, addData, redirectAfterPostGet
import sys
from datetime import date


@login_required
@secure_module
def scheduleConferenceView(request):
    data = {'titulo': 'Horarios de Conferencia',
            'modulo': 'Conferencia',
            'ruta': request.path,
            'fecha': str(date.today())
            }
    model = ScheduleConference
    Formulario = ScheduleConferenceForm
    conference = request.session['conference']

    if request.method == 'POST':
        res_json = []
        action = request.POST['action']
        try:
            with transaction.atomic():
                if action == 'add':
                    form = Formulario(request.POST, request=request)
                    if form.is_valid():
                        form.instance.conference = conference
                        form.save()
                        log(f"Registró un horario de conferencia {form.instance.__str__()}", request, "add",
                            obj=form.instance.id)
                        messages.success(request, "Categoría de tema agregada exitosamente")
                        res_json.append({'error': False, "to": redirectAfterPostGet(request)})
                    else:
                        raise FormError(form)

                elif action == 'change':
                    filtro = model.objects.get(pk=int(request.POST['pk']))
                    form = Formulario(request.POST, instance=filtro, request=request)
                    if form.is_valid() and filtro:
                        form.save()
                        log(f"Editó un horario de conferencia {filtro.__str__()}", request, "change", obj=filtro.id)
                        messages.success(request, "Categoría de tema modificada con éxito")
                        res_json.append({'error': False, "to": redirectAfterPostGet(request)})
                    else:
                        raise FormError(form)

                elif action == 'delete':
                    filtro = model.objects.get(pk=int(request.POST['id']))
                    filtro.status = False
                    filtro.save()
                    log(f"Eliminó un horario de conferencia {filtro.__str__()}", request, "del", obj=filtro.id)
                    messages.success(request, "Categoría de tema eliminada exitosamente")
                    res_json.append({'error': False})

                if action == 'adddetail':
                    filtro = model.objects.get(pk=int(request.POST['pk']))
                    form = DetailScheduleConferenceForm(request.POST, request=request)
                    if form.is_valid():
                        form.instance.cab = filtro
                        form.save()
                        log(f"Registró un nuevo detalle de horario {form.instance.__str__()}", request, "add", obj=form.instance.id)
                        messages.success(request, "Tema agregado exitosamente")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)

                elif action == 'changedetail':
                    filtro = DetailScheduleConference.objects.get(pk=int(request.POST['pk']))
                    form = DetailScheduleConferenceForm(request.POST, instance=filtro, request=request)
                    if form.is_valid() and filtro:
                        form.save()
                        log(f"Editó un nuevo detalle de horario {filtro.__str__()}", request, "change", obj=filtro.id)
                        messages.success(request, "Tema modificado con éxito")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)

                elif action == 'deletedetail':
                    filtro = DetailScheduleConference.objects.get(pk=int(request.POST['id']))
                    filtro.status = False
                    filtro.save()
                    log(f"Eliminó un nuevo detalle de horario {filtro.__str__()}", request, "del", obj=filtro.id)
                    messages.success(request, "Tema eliminado exitosamente")
                    res_json.append({'error': False})

        except ValueError as ex:
            res_json.append({'error': True, "message": str(ex)})
        except FormError as ex:
            res_json.append(ex.dict_error)
        except Exception as ex:
            salva_logs(request, __file__, request.method, action, type(ex).__name__,
                       'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), ex)
            res_json.append({'error': True, "message": "Intente nuevamente"})

        return JsonResponse(res_json, safe=False)

    elif request.method == 'GET':
        addData(request, data)
        if 'action' in request.GET:
            data["action"] = action = request.GET['action']
            if action == 'add':
                data["form"] = Formulario()
                template = get_template("conference/schedule/form.html")
                return JsonResponse({"result": True, 'data': template.render(data)})

            elif action == 'change':
                pk = int(request.GET['id'])
                data['filtro'] = filtro = model.objects.get(pk=pk)
                data["id"] = pk
                data["form"] = Formulario(instance=filtro)
                template = get_template("conference/schedule/form.html")
                return JsonResponse({"result": True, 'data': template.render(data)})

            elif action == 'details':
                try:
                    # Filtrado y listado
                    data['cab'] = cab = model.objects.get(pk=int(request.GET['id']))
                    data['titulo'] = f'Detalles del horario {cab.__str__()}'
                    criterio, filtros, url_vars = request.GET.get('criterio', '').strip(), Q(status=True, cab=cab), f'&action={action}&id={cab.pk}'
                    if criterio:
                        filtros = filtros & Q(title__icontains=criterio)
                        data["criterio"] = criterio
                        url_vars += '&criterio=' + criterio

                    listado = DetailScheduleConference.objects.filter(filtros)
                    data["list_count"] = listado.count()
                    data["url_vars"] = url_vars
                    paginador(request, listado.order_by('-order'), 20, data, url_vars)
                    return render(request, 'conference/schedule/detail/listado.html', data)
                except Exception as ex:
                    pass

            elif action == 'adddetail':
                data['filtro'] = model.objects.get(pk=int(request.GET['id']))
                data["form"] = DetailScheduleConferenceForm()
                template = get_template("conference/schedule/detail/form.html")
                return JsonResponse({"result": True, 'data': template.render(data)})

            elif action == 'changedetail':
                pk = int(request.GET['id'])
                data['filtro'] = filtro = DetailScheduleConference.objects.get(pk=pk)
                data["form"] = DetailScheduleConferenceForm(instance=filtro)
                template = get_template("conference/schedule/detail/form.html")
                return JsonResponse({"result": True, 'data': template.render(data)})

        # Filtrado y listado
        criterio, filtros, url_vars = request.GET.get('criterio', '').strip(), Q(status=True, conference=conference), ''
        if criterio:
            filtros = filtros & Q(title__icontains=criterio)
            data["criterio"] = criterio
            url_vars += '&criterio=' + criterio

        listado = model.objects.filter(filtros)
        data["list_count"] = listado.count()
        data["url_vars"] = url_vars
        paginador(request, listado.order_by('-order'), 20, data, url_vars)
        return render(request, 'conference/schedule/listado.html', data)
