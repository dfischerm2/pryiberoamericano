from django.urls import path, re_path

from .cambiar_sesion_view import cambiarSesionView, regresarSesionView
from .view_arbol_modulogrupo import arbol_modulo_grupo
from .view_auditoria import auditoria
from .view_configuracion import configuracion
from .view_configuracion_es import configuracionEs
from .view_grupo import grupo
from .view_grupourls import grupoUrlsView
from .view_modulo import modulo
from .view_modulogrupo import modulo_grupo
from .view_redes_sociales import redesSocialesView

seguridad_urls = (
    {
        "nombre": "Administración del Sitio",
        "url": 'configuracion/',
        "vista": configuracion,
    },
{
        "nombre": "Administración del Sitio Español",
        "url": 'configuracion-es/',
        "vista": configuracionEs,
    },
    {
        "nombre": "Roles de Usuario",
        "url": 'grupo/',
        "vista": grupo,
    },
    {
        "nombre": "Urls",
        "url": 'modulo/',
        "vista": modulo,
    },
    {
        "nombre": "Administrar Sidebar",
        "url": 'modulogrupo/',
        "vista": modulo_grupo,
    },
    {
        "nombre": "Árbol Sidebar",
        "url": 'arbol-de-grupos-url/',
        "vista": arbol_modulo_grupo
    },
    {
        "nombre": "Auditoría",
        "url": 'auditoria/',
        "vista": auditoria,
    },
    {
        "nombre": "Social Media",
        "url": 'social-media/',
        "vista": redesSocialesView,
    },
)

urlpatterns = [
    path('grupo/urls/<int:pk>/<slug:slug_name>/', grupoUrlsView),
    path('cambiar-sesion/', cambiarSesionView),
    path('regresar-sesion/', regresarSesionView),
]

for u in seguridad_urls:
    urlpatterns.append(re_path(r'^{}$'.format(u["url"]), u["vista"]))
