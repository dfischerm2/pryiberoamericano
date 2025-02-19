from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import Value
from django.db.models.functions import Concat
from core.custom_models import ModelFormBase
from seguridad.models import Configuracion, Modulo, ModuloGrupo, GroupModulo, RedesSociales, ConfiguracionEspanol


class ConfiguracionForm(ModelFormBase):
    class Meta:
        model = Configuracion
        exclude = ('usuario_modificacion', 'fecha_modificacion', 'usuario_creacion',  'fondo_perfil', 'banner_login',)

    def __init__(self, *args, **kwargs):
        super(ConfiguracionForm, self).__init__(*args, **kwargs)
        self.fields["ico"].widget.attrs['data-default-file'] = self.instance.ico.url if self.instance.ico else ""
        self.fields["logo_sistema"].widget.attrs['data-default-file'] = self.instance.logo_sistema.url if self.instance.logo_sistema else ""
        self.fields["logo_sistema_white"].widget.attrs['data-default-file'] = self.instance.logo_sistema_white.url if self.instance.logo_sistema_white else ""
        # self.fields["imagenprincipal"].widget.attrs['data-default-file'] = self.instance.imagenprincipal.url if self.instance.imagenprincipal else ""
        self.fields["fondoprincipal"].widget.attrs['data-default-file'] = self.instance.fondoprincipal.url if self.instance.fondoprincipal else ""
        self.fields['ico'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"
        self.fields['logo_sistema'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"
        self.fields['logo_sistema_white'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"
        # self.fields['imagenprincipal'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"
        self.fields['fondoprincipal'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"

        for k, v in self.fields.items():
            if k in ('ico', 'logo_sistema', 'logo_sistema_white', 'direccion', 'fondoprincipal', 'nombre_empresa', 'alias', 'descripcion', 'telefono', 'email',  'email_notificacion', 'textoprincipal', 'textosecundario', 'web', 'logo_investigacion_unemi', 'logo_unemi',):
                self.fields[k].widget.attrs['col'] = "6"
            if k in ('telefono', 'telefono_emergencia'):
                self.fields[k].widget.attrs['pattern'] = "\d*"
                self.fields[k].widget.attrs['title'] = "Sólo números"
                self.fields[k].widget.attrs['onKeyPress'] = "return soloNumeros(event)"
                self.fields[k].widget.attrs['pattern'] = "\d*"
            if k in ('valor_mensual', 'valor_anual'):
                self.fields[k].widget.attrs['title'] = "Sólo números"
                self.fields[k].widget.attrs['onKeyPress'] = "return soloNumeros1(event)"
            if k in ('descripcion_landing',):
                self.fields[k].widget.attrs['col'] = "12"
                self.fields[k].widget.attrs['rows'] = "3"


class ConfiguracionEspanolForm(ModelFormBase):
    class Meta:
        model = ConfiguracionEspanol
        exclude = ('usuario_modificacion', 'fecha_modificacion', 'usuario_creacion',  'fondo_perfil', 'banner_login',)

    def __init__(self, *args, **kwargs):
        super(ConfiguracionEspanolForm, self).__init__(*args, **kwargs)
        self.fields["ico"].widget.attrs['data-default-file'] = self.instance.ico.url if self.instance.ico else ""
        self.fields["logo_sistema"].widget.attrs['data-default-file'] = self.instance.logo_sistema.url if self.instance.logo_sistema else ""
        self.fields["logo_sistema_white"].widget.attrs['data-default-file'] = self.instance.logo_sistema_white.url if self.instance.logo_sistema_white else ""
        # self.fields["imagenprincipal"].widget.attrs['data-default-file'] = self.instance.imagenprincipal.url if self.instance.imagenprincipal else ""
        self.fields["fondoprincipal"].widget.attrs['data-default-file'] = self.instance.fondoprincipal.url if self.instance.fondoprincipal else ""
        self.fields['ico'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"
        self.fields['logo_sistema'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"
        self.fields['logo_sistema_white'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"
        # self.fields['imagenprincipal'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"
        self.fields['fondoprincipal'].widget.attrs['data-allowed-file-extensions'] = "jpg jpeg png tiff svg jfif"

        for k, v in self.fields.items():
            if k in ('ico', 'logo_sistema', 'logo_sistema_white', 'direccion', 'fondoprincipal', 'nombre_empresa', 'alias', 'descripcion', 'telefono', 'email',  'email_notificacion', 'textoprincipal', 'textosecundario', 'web', 'logo_investigacion_unemi', 'logo_unemi',):
                self.fields[k].widget.attrs['col'] = "6"
            if k in ('telefono', 'telefono_emergencia'):
                self.fields[k].widget.attrs['pattern'] = "\d*"
                self.fields[k].widget.attrs['title'] = "Sólo números"
                self.fields[k].widget.attrs['onKeyPress'] = "return soloNumeros(event)"
                self.fields[k].widget.attrs['pattern'] = "\d*"
            if k in ('valor_mensual', 'valor_anual'):
                self.fields[k].widget.attrs['title'] = "Sólo números"
                self.fields[k].widget.attrs['onKeyPress'] = "return soloNumeros1(event)"
            if k in ('descripcion_landing',):
                self.fields[k].widget.attrs['col'] = "12"
                self.fields[k].widget.attrs['rows'] = "3"


class ModuloForm(ModelFormBase):
    class Meta:
        model = Modulo
        exclude = ( 'usuario_modificacion', 'fecha_modificacion', 'usuario_creacion', 'fecha_registro', 'status')


class GroupForm(ModelFormBase):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].queryset = self.fields['permissions'].queryset.\
            annotate(full_name_db=Concat('content_type__app_label', Value('__'), 'content_type__model')).\
            exclude(full_name_db__in=['sessions__session', 'auth__permission', 'contenttypes__contenttype',
                                     'admin__logentry', 'authtoken__token', 'seguridad__usuarioconectado', 'seguridad__carousel', 'seguridad__redsocial', 'seguridad__errorlog', 'seguridad__audiusuariotabla',
                                     'background_task__completedtask', 'background_task__task', 'webpush__subscriptioninfo',
                                      'webpush__pushinformation', 'webpush__group', 'authtoken__tokenproxy', 'ventas__pedidodetalle',
                                      'autenticacion__codigo', 'seguridad__usuarionotificacion', 'seguridad__sessionuser']).\
            exclude(content_type__app_label__in=("dobra", "reportes"))


class ModuloGrupoForm(ModelFormBase):
    class Meta:
        model = ModuloGrupo
        exclude = ( 'usuario_modificacion', 'fecha_modificacion', 'usuario_creacion', 'fecha_registro', 'status')

    def __init__(self, *args, **kwargs):
        kwargs["no_requeridos"] = ["modulos"]
        super(ModuloGrupoForm, self).__init__(*args, **kwargs)
        self.fields['modulos'].queryset = self.fields['modulos'].queryset.order_by('orden')
        self.fields['modulos'].widget = forms.HiddenInput()
        self.initial["modulos"] = ""


class GroupModuloForm(ModelFormBase):
    class Meta:
        model = GroupModulo
        exclude = ( 'usuario_modificacion', 'fecha_modificacion', 'usuario_creacion', 'fecha_registro', 'status')

    def __init__(self, *args, **kwargs):
        kwargs["no_requeridos"] = ["modulos"]
        super(GroupModuloForm, self).__init__(*args, **kwargs)
        self.fields['modulos'].queryset = self.fields['modulos'].queryset.order_by('orden')
        self.fields["group"].widget = forms.HiddenInput()


class RedesSocialesForm(ModelFormBase):
    class Meta:
        model = RedesSociales
        exclude = ('usuario_creacion', 'fecha_registro', 'hora_registro', 'status', 'usuario_modificacion','conference',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver') if 'ver' in kwargs else False
        instancia = kwargs["instance"] if 'instance' in kwargs else None
        super(RedesSocialesForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"
            if k in ('publicar',):
                self.fields[k].widget.attrs['class'] = "js-switch"
                self.fields[k].widget.attrs['data-render'] = "switchery"
                self.fields[k].widget.attrs['data-theme'] = "default"
                self.fields[k].widget.attrs['col'] = "3"