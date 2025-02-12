
from django.urls import path, re_path

from public.acerade import acercade
from public.view_changepass import changepass

#from .view_pago import pagoView
from public.view_registro import registerView
from public.view_restaurar import restaurar
from public.view_recordarusername import recordarusername
from public.view_perfil import perfil

from .view_login import login_tienda, logout_tienda
from .view_conferences import conferences
from .view_members import members
from .index import indexEs

urlpatterns = [
    # path('', index),
    path('', indexEs),
    path('members/', members),
path('previous-events/', conferences),
    re_path(r'^acercade/', acercade),
    #path('pago/<str:pedido_id>/', pagoView),
    re_path(r'^perfil/', perfil),
    # url(r'^register/', registro),
    re_path(r'^login/', login_tienda),
    re_path(r'^logout/', logout_tienda),
    re_path(r'^restorepass/', restaurar),
    re_path(r'^restoreusername/', recordarusername),
    re_path(r'^changepass/', changepass),
    re_path(r'^register/', registerView),

]
