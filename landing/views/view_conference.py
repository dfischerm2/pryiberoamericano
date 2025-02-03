from datetime import date
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from core.custom_models import FormError
from core.funciones import addData, paginador, secure_module, log
from django.contrib import messages

from landing.forms import ConferenceForm, ItemDetailConferenceForm, PhotoCatalogConferenceForm, \
    LandingConfereceCarouselForm
from landing.models import Conference, ItemDetailConference, PhotoCatalogConference, LandingConfereceCarousel


@login_required
@secure_module
def conferenceView(request):
    data = {
        'titulo': 'Conference',
        'modulo': 'Landing',
        'ruta': request.path,
        'fecha': str(date.today())
    }
    addData(request, data)
    model = Conference
    Formulario = ConferenceForm
    if request.method == 'POST':
        res_json = []
        action = request.POST['action']
        try:
            with transaction.atomic():
                if action == 'add':
                    form = Formulario(request.POST, request.FILES, request=request)
                    if form.is_valid():
                        form.save()
                        log(f"Registro un evento {form.instance.__str__()}", request, "add")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)
                elif action == 'change':
                    filtro = model.objects.get(pk=int(request.POST['pk']))
                    form = Formulario(request.POST, request.FILES, request=request, instance=filtro)
                    if form.is_valid() and filtro:
                        form.save()
                        log(f"Edito un evento {form.instance.__str__()}", request, "change")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)
                elif action == 'delete':
                    filtro = model.objects.get(pk=int(request.POST['id']))
                    filtro.status = False
                    filtro.save(request)
                    log(f"Elimino un evento {filtro.__str__()}", request, "delete")
                    messages.success(request, f"Registro Eliminado")
                    res_json = {"error": False}
                elif action == 'checkactive':
                    pk, estado = request.POST['id'], request.POST['val']
                    mensaje = 'Conferencia Activada' if estado == 'true' else 'Conferencia Desactivada'
                    retorno = 1 if estado == 'true' else 2
                    qsbase = model.objects.get(pk=pk)
                    qsbase.active = True if retorno == 1 else False
                    qsbase.save()
                    res_json = {'result': True, 'mensaje': mensaje, 'retorno': retorno}
                if action == 'additem':
                    filtro = model.objects.get(pk=int(request.POST['pk']))
                    form = ItemDetailConferenceForm(request.POST, request.FILES, request=request)
                    if form.is_valid():
                        form.instance.conference = filtro
                        form.save()
                        log(f"Registro un item de conferencia {form.instance.__str__()}", request, "add")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)
                elif action == 'changeitem':
                    filtro = ItemDetailConference.objects.get(pk=int(request.POST['pk']))
                    form = ItemDetailConferenceForm(request.POST, request.FILES, request=request, instance=filtro)
                    if form.is_valid() and filtro:
                        form.save()
                        log(f"Edito un item de conferencia {form.instance.__str__()}", request, "change")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)
                elif action == 'deleteitem':
                    filtro = ItemDetailConference.objects.get(pk=int(request.POST['id']))
                    filtro.status = False
                    filtro.save(request)
                    log(f"Elimino un item de conferencia {filtro.__str__()}", request, "delete")
                    messages.success(request, f"Registro Eliminado")
                    res_json = {"error": False}
                if action == 'addcatalog':
                    filtro = model.objects.get(pk=int(request.POST['pk']))
                    form = PhotoCatalogConferenceForm(request.POST, request.FILES, request=request)
                    if form.is_valid():
                        form.instance.conference = filtro
                        form.save()
                        log(f"Registro un catalog de conferencia {form.instance.__str__()}", request, "add")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)
                elif action == 'changecatalog':
                    filtro = PhotoCatalogConference.objects.get(pk=int(request.POST['pk']))
                    form = PhotoCatalogConferenceForm(request.POST, request.FILES, request=request, instance=filtro)
                    if form.is_valid() and filtro:
                        form.save()
                        log(f"Edito un catalog de conferencia {form.instance.__str__()}", request, "change")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)
                elif action == 'deletecatalog':
                    filtro = PhotoCatalogConference.objects.get(pk=int(request.POST['id']))
                    filtro.status = False
                    filtro.save(request)
                    log(f"Elimino un catalog de conferencia {filtro.__str__()}", request, "delete")
                    messages.success(request, f"Registro Eliminado")
                    res_json = {"error": False}
                elif action == 'checkpubliccatalog':
                    pk, estado = request.POST['id'], request.POST['val']
                    mensaje = 'Catalogo Activado' if estado == 'true' else 'Catalogo Desactivado'
                    retorno = 1 if estado == 'true' else 2
                    qsbase = PhotoCatalogConference.objects.get(pk=pk)
                    qsbase.public = True if retorno == 1 else False
                    qsbase.save()
                    res_json = {'result': True, 'mensaje': mensaje, 'retorno': retorno}
                if action == 'addcarrousel':
                    filtro = model.objects.get(pk=int(request.POST['pk']))
                    form = LandingConfereceCarouselForm(request.POST, request.FILES, request=request)
                    if form.is_valid():
                        form.instance.conference = filtro
                        form.save()
                        log(f"Registro una imagen carrousel de conferencia {form.instance.__str__()}", request, "add")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)
                elif action == 'changecarrousel':
                    filtro = LandingConfereceCarousel.objects.get(pk=int(request.POST['pk']))
                    form = LandingConfereceCarouselForm(request.POST, request.FILES, request=request, instance=filtro)
                    if form.is_valid() and filtro:
                        form.save()
                        log(f"Edito una imagen carrousel de conferencia {form.instance.__str__()}", request, "change")
                        res_json.append({'error': False, "reload": True})
                    else:
                        raise FormError(form)
                elif action == 'deletecarrousel':
                    filtro = LandingConfereceCarousel.objects.get(pk=int(request.POST['id']))
                    filtro.status = False
                    filtro.save(request)
                    log(f"Elimino una imagen carrousel de conferencia {filtro.__str__()}", request, "delete")
                    messages.success(request, f"Registro Eliminado")
                    res_json = {"error": False}
                elif action == 'checkpubliccarrousel':
                    pk, estado = request.POST['id'], request.POST['val']
                    mensaje = 'Imagen Activada' if estado == 'true' else 'Imagen Desactivada'
                    retorno = 1 if estado == 'true' else 2
                    qsbase = LandingConfereceCarousel.objects.get(pk=pk)
                    qsbase.public = True if retorno == 1 else False
                    qsbase.save()
                    res_json = {'result': True, 'mensaje': mensaje, 'retorno': retorno}


        except ValueError as ex:
            res_json.append({'error': True, "message": str(ex)})
        except FormError as ex:
            res_json.append(ex.dict_error)
        except Exception as ex:
            res_json.append({'error': True, "message": f"Intente Nuevamente: {ex}"})
        return JsonResponse(res_json, safe=False)
    elif request.method == 'GET':
        if 'action' in request.GET:
            data["action"] = action = request.GET['action']
            if action == 'add':
                try:
                    form = Formulario()
                    data['form'] = form
                    template = get_template("conference/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    return JsonResponse({"result": False, 'message': str(ex)})
            elif action == 'change':
                try:
                    data['id'] = id = int(request.GET['id'])
                    data['filtro'] = filtro = model.objects.get(pk=id)
                    form = Formulario(instance=filtro)
                    data['form'] = form
                    template = get_template("conference/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    return JsonResponse({"result": False, 'message': str(ex)})
            elif action == 'items':
                data['cab'] = cab = model.objects.get(pk=int(request.GET['id']))
                data['titulo'] = f'Items de {cab.title}'
                criterio, filtros, url_vars = request.GET.get('criterio','').strip(), Q(
                    status=True, conference=cab), f'&action={action}&id={cab.pk}'
                if criterio:
                    filtros = filtros & (Q(principal_text__icontains=criterio))
                    data["criterio"] = criterio
                    url_vars += '&criterio=' + criterio
                listado = ItemDetailConference.objects.filter(filtros)
                data["list_count"] = listado.count()
                data["url_vars"] = url_vars
                paginador(request, listado.order_by('-id'), 20, data, url_vars)
                return render(request, 'conference/items/listado.html', data)
            elif action == 'additem':
                try:
                    data['filtro'] = model.objects.get(pk=int(request.GET['id']))
                    form = ItemDetailConferenceForm()
                    data['form'] = form
                    template = get_template("conference/items/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    return JsonResponse({"result": False, 'message': str(ex)})
            elif action == 'changeitem':
                try:
                    data['id'] = id = int(request.GET['id'])
                    data['filtro'] = filtro = ItemDetailConference.objects.get(pk=id)
                    form = ItemDetailConferenceForm(instance=filtro)
                    data['form'] = form
                    template = get_template("conference/items/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    return JsonResponse({"result": False, 'message': str(ex)})
            elif action == 'catalog':
                data['cab'] = cab = model.objects.get(pk=int(request.GET['id']))
                data['titulo'] = f'Catalogo de {cab.title}'
                criterio, filtros, url_vars = request.GET.get('criterio','').strip(), Q(
                    status=True, conference=cab), f'&action={action}&id={cab.pk}'
                if criterio:
                    filtros = filtros & (Q(principal_text__icontains=criterio))
                    data["criterio"] = criterio
                    url_vars += '&criterio=' + criterio
                listado = PhotoCatalogConference.objects.filter(filtros)
                data["list_count"] = listado.count()
                data["url_vars"] = url_vars
                paginador(request, listado.order_by('-id'), 20, data, url_vars)
                return render(request, 'conference/catalog/listado.html', data)
            elif action == 'addcatalog':
                try:
                    data['filtro'] = model.objects.get(pk=int(request.GET['id']))
                    form = PhotoCatalogConferenceForm()
                    data['form'] = form
                    template = get_template("conference/catalog/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    return JsonResponse({"result": False, 'message': str(ex)})
            elif action == 'changecatalog':
                try:
                    data['id'] = id = int(request.GET['id'])
                    data['filtro'] = filtro = PhotoCatalogConference.objects.get(pk=id)
                    form = PhotoCatalogConferenceForm(instance=filtro)
                    data['form'] = form
                    template = get_template("conference/catalog/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    return JsonResponse({"result": False, 'message': str(ex)})
            elif action == 'carrousel':
                data['cab'] = cab = model.objects.get(pk=int(request.GET['id']))
                data['titulo'] = f'Carrusel de {cab.title}'
                criterio, filtros, url_vars = request.GET.get('criterio','').strip(), Q(
                    status=True, conference=cab), f'&action={action}&id={cab.pk}'
                if criterio:
                    filtros = filtros & (Q(principal_text__icontains=criterio))
                    data["criterio"] = criterio
                    url_vars += '&criterio=' + criterio
                listado = LandingConfereceCarousel.objects.filter(filtros)
                data["list_count"] = listado.count()
                data["url_vars"] = url_vars
                paginador(request, listado.order_by('-id'), 20, data, url_vars)
                return render(request, 'conference/carrousel/listado.html', data)
            elif action == 'addcarrousel':
                try:
                    data['filtro'] = model.objects.get(pk=int(request.GET['id']))
                    form = LandingConfereceCarouselForm()
                    data['form'] = form
                    template = get_template("conference/carrousel/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    return JsonResponse({"result": False, 'message': str(ex)})
            elif action == 'changecarrousel':
                try:
                    data['id'] = id = int(request.GET['id'])
                    data['filtro'] = filtro = LandingConfereceCarousel.objects.get(pk=id)
                    form = LandingConfereceCarouselForm(instance=filtro)
                    data['form'] = form
                    template = get_template("conference/carrousel/form.html")
                    return JsonResponse({"result": True, 'data': template.render(data)})
                except Exception as ex:
                    return JsonResponse({"result": False, 'message': str(ex)})


        id, criterio, filtros, url_vars = request.GET.get('id', '').strip(), request.GET.get('criterio', '').strip(), Q(status=True), ''
        if id:
            filtros = filtros & (Q(id=id))
            data["id"] = id
            url_vars += '&id=' + id
        if criterio:
            filtros = filtros & (Q(title__icontains=criterio))
            data["criterio"] = criterio
            url_vars += '&criterio=' + criterio
        listado = model.objects.filter(filtros)
        data["list_count"] = listado.count()
        data["url_vars"] = url_vars
        paginador(request, listado.order_by('-active','-end_date'), 20, data, url_vars)
        return render(request, 'conference/listado.html', data)