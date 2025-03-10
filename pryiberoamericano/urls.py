"""
   Django 4.1
"""
from django.contrib import admin
from django.urls import path

from area_geografica.urls import area_geografica_urls
from core.funciones import db_table_exists
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.views.generic import RedirectView
from django.views.static import serve

from autenticacion.urls import autenticacion_urls
from autenticacion.view_perfil import perfilView
from core.ajax import ConsultasAjax
from financiero.urls import financiero_urls
from landing.urls import landing_urls
from pedidos.urls import pedidos_urls
from pryiberoamericano.view_clearsitedata import clearSiteDataView
from pryiberoamericano import settings
from pryiberoamericano.view_redirect import redirectView, redirectToUrlView
from public.check_language import check_language
from seguridad.models import Configuracion, Modulo
from seguridad.urls import seguridad_urls
from seguridad.view_index import index
from django.conf.urls.static import static
from core.consultas import consultas


confi = Configuracion.get_instancia()
icon_url = confi.ico.url if confi.ico else ""
favicon_view = RedirectView.as_view(url=icon_url, permanent=True)
urls_sistema = (
    {
        "nombre": "Áreas Geográficas",
        "url": "area-geografica/",
        "sub_urls": area_geografica_urls,
        "include": include('area_geografica.urls'),
        "name": None,
        "vista": None
    },
    {
        "nombre": "Autenticación",
        "url": 'autenticacion/',
        "sub_urls": autenticacion_urls,
        "include": include('autenticacion.urls'),
        "name": None,
        "vista": None
    },
    {
        "nombre": "Seguridad",
        "url": 'seguridad/',
        "sub_urls": seguridad_urls,
        "include": include('seguridad.urls'),
        "name": None,
        "vista": None
    },
    {
        "nombre": "Landing",
        "url": 'landing/',
        "sub_urls": landing_urls,
        "include": include('landing.urls'),
        "name": None,
        "vista": None
    },
    {
        "nombre": "Financiero",
        "url": "financiero/",
        "sub_urls": financiero_urls,
        "include": include('financiero.urls'),
        "name": None,
        "vista": None
    },
    {
        "nombre": "Pedidos",
        "url": "pedidos/",
        "sub_urls": pedidos_urls,
        "include": include('pedidos.urls'),
        "name": None,
        "vista": None
    },
)
urlpatterns = [
    path('set-language/', set_language, name='set_language'),
    path('check-language/', check_language, name='check_language'),
    path('panel/', index),
    path('admin/', admin.site.urls),
]
urlpatterns += i18n_patterns (

    path('perfilpanel/', perfilView),
    path('consultas/', consultas, name='Consultas API'),
    path('ajaxrequest/', ConsultasAjax.as_view(), name='Ajax Consultas v1'),
    path('ajaxrequest/<slug:accion>', ConsultasAjax.as_view(), name='Ajax Consultas v1'),
    path('ajaxrequest/<slug:accion>/<str:pk>', ConsultasAjax.as_view(), name='Ajax Consultas v1'),
    path('redirect-to-url/<int:pk>/', redirectToUrlView),
    # urls apache
    re_path(r'^favicon\.ico', favicon_view),
    path('clear-site-data/', clearSiteDataView),
    # select2
    path("select2/", include("django_select2.urls")),
    path('', include('public.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
                    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), ]

for u in urls_sistema:
    if u["vista"] and not u["include"]:
        if u["name"]:
            urlpatterns.append(path('{}'.format(u["url"]), u["vista"], name=u["name"]))
        else:
            urlpatterns.append(path('{}'.format(u["url"]), u["vista"]))
    elif not u["vista"] and u["include"]:
        if u["name"]:
            urlpatterns.append(path('{}'.format(u["url"]), u["include"], name=u["name"]))
        else:
            urlpatterns.append(path('{}'.format(u["url"]), u["include"]))

if db_table_exists(Modulo._meta.db_table):
    qs_modulos = Modulo.objects.filter(status=True)
    for u in urls_sistema:
        url = "/{}".format(u["url"])
        modulos = qs_modulos.filter(url__startswith=url)
        if u["sub_urls"]:
            for su in u["sub_urls"]:
                mod_url = "/{}{}".format(u["url"], su["url"])
                if modulos.filter(url=mod_url).exists():
                    mod = modulos.filter(url=mod_url).first()
                    if mod.nombre != su["nombre"]:
                        mod.nombre = su["nombre"]
                        mod.save()

admin.site.site_header = "{} {}".format("Administración", "pryiberoamericano")
admin.site.site_title = "{} {}".format("Administración", "pryiberoamericano")
