
from django.urls import path, re_path

from .acerade import acercade
from .index import index
from .index2 import index2
from .view_changepass import changepass
from .view_conferences import conferences
from .view_members import members

from .view_registro import registerView
from .view_restaurar import restaurar
from .view_login import login_tienda, logout_tienda
from .view_recordarusername import recordarusername
from .view_perfil import perfil
app_name = "public"
urlpatterns = [
    path("", index2, name="home"),
    path("original/", index, name="home2"),
    path("members/", members, name="members"),
    path("previous-events/", conferences, name="previous_events"),
    path("acercade/", acercade, name="acercade"),
    path("perfil/", perfil, name="perfil"),
    path("login/", login_tienda, name="login"),
    path("logout/", logout_tienda, name="logout"),
    path("restorepass/", restaurar, name="restorepass"),
    path("restoreusername/", recordarusername, name="restoreusername"),
    path("changepass/", changepass, name="changepass"),
    path("register/", registerView, name="register"),
]
