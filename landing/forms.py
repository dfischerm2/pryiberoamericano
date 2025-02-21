from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from .models import TopicCategory, Topic, CommitteeCategory, \
    CommitteeMember, Conference, \
    ConferenceFee, DetailConferenceFee, ItemDetailConference, PhotoCatalogConference, LandingConfereceCarousel, \
    ScheduleConference, DetailScheduleConference, ImportantDates
from core.custom_models import ModelFormBase


class TopicCategoryForm(ModelFormBase):
    class Meta:
        model = TopicCategory
        fields = ('name', 'description', 'icon', 'public',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(TopicCategoryForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"
            if k in ('public',):
                self.fields[k].widget.attrs['class'] = "js-switch"
                self.fields[k].widget.attrs['data-render'] = "switchery"
                self.fields[k].widget.attrs['data-theme'] = "default"
                self.fields[k].widget.attrs['col'] = "3"
            if k in ('conference',):
                self.fields[k].widget.attrs['class'] = "form-control select2-simple"
            if k in ('description', 'name',):
                self.fields[k].widget.attrs['col'] = "12"
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'


class TopicCategoryFormESP(ModelFormBase):
    class Meta:
        model = TopicCategory
        fields = ('name_esp', 'description_esp',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(TopicCategoryFormESP, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"
            if k in ('description_esp', 'name_esp',):
                self.fields[k].widget.attrs['col'] = "12"
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'


class TopicForm(ModelFormBase):
    class Meta:
        model = Topic
        fields = ('name', 'public',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(TopicForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            if k == 'category':  # Aplica jselect2 solo al campo ForeignKey
                self.fields[k].widget.attrs['class'] = "jselect2"
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'

class TopicFormESP(ModelFormBase):
    class Meta:
        model = Topic
        fields = ('name_esp',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(TopicFormESP, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"


class ScheduleConferenceForm(ModelFormBase):
    class Meta:
        model = ScheduleConference
        fields = ('title', 'order', 'date_start', 'date_end', 'date_str')

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(ScheduleConferenceForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"
            if k in ('description', 'name',):
                self.fields[k].widget.attrs['col'] = "12"
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'


class DetailScheduleConferenceForm(ModelFormBase):
    class Meta:
        model = DetailScheduleConference
        fields = ('title', 'description', 'time_start', 'time_end', 'order')

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(DetailScheduleConferenceForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"
            if k in ('description', 'title',):
                self.fields[k].widget.attrs['col'] = "12"
            if k in ('description',):
                self.fields[k].widget.attrs['class'] = "summernote"
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'


class DetailScheduleConferenceFormESP(ModelFormBase):
    class Meta:
        model = DetailScheduleConference
        fields = ('description_esp',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(DetailScheduleConferenceFormESP, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"
            if k in ('description_esp',):
                self.fields[k].widget.attrs['col'] = "12"
                self.fields[k].widget.attrs['class'] = "summernote"
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'


class CommitteeCategoryForm(ModelFormBase):
    class Meta:
        model = CommitteeCategory
        fields = ('name', 'order', 'active', 'public',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(CommitteeCategoryForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"
            if k in ('active', 'public',):
                self.fields[k].widget.attrs['class'] = "js-switch"
                self.fields[k].widget.attrs['data-render'] = "switchery"
                self.fields[k].widget.attrs['data-theme'] = "default"
                self.fields[k].widget.attrs['col'] = "3"
            if k in ('conference',):
                self.fields[k].widget.attrs['class'] = "jselect2"
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'


class CommitteeMemberForm(ModelFormBase):
    class Meta:
        model = CommitteeMember
        fields = ('name', 'sexo', 'degree','linkedin', 'rol', 'description_rol', 'photo' , 'order', 'public',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(CommitteeMemberForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            if k in ['category', 'sexo']:  # Aplica jselect2 solo al campo ForeignKey
                self.fields[k].widget.attrs['class'] = "jselect2"
            if k in ['category', 'sexo', 'degree', 'rol', 'linkedin', 'x', 'instagram', 'facebook', 'youtube', 'public', 'order']:
                self.fields[k].widget.attrs['col'] = "6"
            if k in('photo'):
                self.fields[k].widget.attrs['class'] = 'dropify'
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'


class CommitteeMemberFormESP(ModelFormBase):
    class Meta:
        model = CommitteeMember
        fields = ('rol_esp', 'description_rol_esp',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver', False)
        self.editando = 'instance' in kwargs
        super(CommitteeMemberFormESP, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['col'] = "12"
            if ver:
                self.fields[k].widget.attrs['disabled'] = 'disabled'


class ConferenceForm(ModelFormBase):
    class Meta:
        model = Conference
        exclude = ('usuario_creacion', 'fecha_registro', 'hora_registro', 'status', 'usuario_modificacion',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver') if 'ver' in kwargs else False
        instancia = kwargs["instance"] if 'instance' in kwargs else None
        super(ConferenceForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"

            if k in ('start_date','end_date','date_str', 'location_str',):
                self.fields[k].widget.attrs['col'] = "6"
            if k in ('title',):
                self.fields[k].widget.attrs['col'] = "11"
            if k in ('number',):
                self.fields[k].widget.attrs['col'] = "1"
            if k in ('active',):
                self.fields[k].widget.attrs['class'] = "js-switch"
                self.fields[k].widget.attrs['data-render'] = "switchery"
                self.fields[k].widget.attrs['data-theme'] = "default"

            if k in ('image_principal',):
                self.fields[k].widget.attrs['class'] = "dropify"


class ConferenceFeeForm(ModelFormBase):
    class Meta:
        model = ConferenceFee
        exclude = ('usuario_creacion', 'fecha_registro', 'hora_registro', 'status', 'usuario_modificacion','conference',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver') if 'ver' in kwargs else False
        instancia = kwargs["instance"] if 'instance' in kwargs else None
        super(ConferenceFeeForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"

            if k in ('role',):
                self.fields[k].widget.attrs['class'] = "form-control select2-simple"

            if k in ('published',):
                self.fields[k].widget.attrs['class'] = "js-switch"
                self.fields[k].widget.attrs['data-render'] = "switchery"
                self.fields[k].widget.attrs['data-theme'] = "default"
                self.fields[k].widget.attrs['col'] = "3"

class ItemDetailConferenceForm(ModelFormBase):
    class Meta:
        model = ItemDetailConference
        exclude = ('usuario_creacion', 'fecha_registro', 'hora_registro', 'status', 'usuario_modificacion','conference',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver') if 'ver' in kwargs else False
        instancia = kwargs["instance"] if 'instance' in kwargs else None
        super(ItemDetailConferenceForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"
            if k in ('color',):
                self.fields[k].widget.input_type = "color"


class PhotoCatalogConferenceForm(ModelFormBase):
    class Meta:
        model = PhotoCatalogConference
        exclude = ('usuario_creacion', 'fecha_registro', 'hora_registro', 'status', 'usuario_modificacion','conference',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver') if 'ver' in kwargs else False
        instancia = kwargs["instance"] if 'instance' in kwargs else None
        super(PhotoCatalogConferenceForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "12"
            if k in ('public',):
                self.fields[k].widget.attrs['class'] = "js-switch"
                self.fields[k].widget.attrs['data-render'] = "switchery"
                self.fields[k].widget.attrs['data-theme'] = "default"
            if k in ('image',):
                self.fields[k].widget.attrs['class'] = "dropify"


class LandingConfereceCarouselForm(ModelFormBase):
    class Meta:
        model = LandingConfereceCarousel
        exclude = ('usuario_creacion', 'fecha_registro', 'hora_registro', 'status', 'usuario_modificacion','conference',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver') if 'ver' in kwargs else False
        instancia = kwargs["instance"] if 'instance' in kwargs else None
        super(LandingConfereceCarouselForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "12"
            if k in ('public',):
                self.fields[k].widget.attrs['class'] = "js-switch"
                self.fields[k].widget.attrs['data-render'] = "switchery"
                self.fields[k].widget.attrs['data-theme'] = "default"
                self.fields[k].widget.attrs['col'] = "3"
            if k in ('image',):
                self.fields[k].widget.attrs['class'] = "dropify"


class DetailConferenceFeeForm(ModelFormBase):
    class Meta:
        model = DetailConferenceFee
        exclude = ('usuario_creacion', 'fecha_registro', 'hora_registro', 'status', 'usuario_modificacion','cab',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver') if 'ver' in kwargs else False
        instancia = kwargs["instance"] if 'instance' in kwargs else None
        super(DetailConferenceFeeForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "12"


class ImportantDatesForm(ModelFormBase):
    class Meta:
        model = ImportantDates
        exclude = ('usuario_creacion', 'fecha_registro', 'hora_registro', 'status', 'usuario_modificacion','conference',)

    def __init__(self, *args, **kwargs):
        ver = kwargs.pop('ver') if 'ver' in kwargs else False
        instancia = kwargs["instance"] if 'instance' in kwargs else None
        super(ImportantDatesForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = "form-control"
            self.fields[k].widget.attrs['col'] = "6"


