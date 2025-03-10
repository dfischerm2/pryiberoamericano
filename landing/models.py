from django.db import models
from core.custom_models import ModeloBase
from django.utils.translation import gettext_lazy as _, get_language


# Create your models here.

class Conference(ModeloBase):
    number = models.CharField(blank=True, null=True, max_length=200, verbose_name='Número')
    title = models.CharField(max_length=200, verbose_name='Título')
    subtitle = models.CharField(max_length=200, verbose_name='Subtítulo')
    start_date = models.DateField(verbose_name='Fecha de Inicio')
    end_date = models.DateField(verbose_name='Fecha de Fin')
    date_str = models.CharField(blank=True, null=True, max_length=200, verbose_name='Fecha en Cadena')
    location_str = models.CharField(blank=True, null=True, max_length=200, verbose_name='Ubicación')
    image_principal = models.ImageField(blank=True, null=True, upload_to='conference/images/', verbose_name='Imagen Principal')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def get_trans_title(self):
        return _(self.title)

    def get_trans_subtitle(self):
        return _(self.subtitle)

    def get_trans_date_str(self):
        return _(self.date_str)

    def get_items(self):
        return self.itemdetailconference_set.filter(status=True).order_by('-id')

    def get_catalog(self):
        return self.photocatalogconference_set.filter(status=True).order_by('-id')

    def get_carousel(self):
        return self.landingconferececarousel_set.filter(status=True).order_by('-id')

    def get_social_medias(self):
        return self.redessociales_set.filter(publicar=True, status=True)

    def get_topics(self):
        return self.topiccategory_set.filter(public=True, status=True)

    def get_active(self):
        return 'text-success fa fa-check-circle' if self.active else 'text-danger fa fa-times-circle'

    def __str__(self):
        return f'{self.number} {self.title}'

    class Meta:
        verbose_name = 'Conference'
        verbose_name_plural = 'Conferences'


class ItemDetailConference(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    principal_text = models.CharField(blank=True, null=True, verbose_name='Texto Principal')
    secondary_text = models.CharField(blank=True, null=True, verbose_name='Texto Secundario')
    color = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name=u"Color")

    def get_trans_secondary_text(self):
        return _(self.secondary_text)

    def __str__(self):
        return f'{self.principal_text} - {self.secondary_text}'

    class Meta:
        verbose_name = 'Item Detail Conference'
        verbose_name_plural = 'Item Detail Conferences'


class PhotoCatalogConference(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='conference/catalog/', verbose_name='Imagen')
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Photo Catalog Conference'
        verbose_name_plural = 'Photo Catalog Conferences'


class LandingConfereceCarousel(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(default=0)
    image = models.ImageField(blank=True, null=True, upload_to='landing_conference_carousel/')
    public = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.conference.title} - {self.order}'


class CommitteeCategory(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    order = models.IntegerField(default=0, null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name='Activo')
    public = models.BooleanField(default=True, verbose_name='Publicado en landing')

    def get_trans_name(self):
        return _(self.name)

    def get_members_all(self):
        return self.members.filter(status=True).order_by('order')

    def get_members(self):
        return self.members.filter(status=True, public=True).order_by('order')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Committee Category'
        verbose_name_plural = 'Committee Categories'
        ordering = ['order']


class CommitteeMember(ModeloBase):
    SEXO = (
        ("MASCULINO", "Masculino"),
        ("FEMENINO", "Femenino"),
        ("NINGUNO", "Sin definir"),
    )
    order = models.IntegerField(blank=True, null=True, verbose_name='Orden')
    category = models.ForeignKey(CommitteeCategory, related_name='members', blank=True, null=True, on_delete=models.CASCADE)
    sexo = models.CharField(verbose_name="Sexo", max_length=50, choices=SEXO, default="NINGUNO",  null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=200, verbose_name='Nombre')
    degree = models.CharField(blank=True, null=True, max_length=100, verbose_name='Grado')
    rol = models.CharField(blank=True, null=True, max_length=500, verbose_name='Rol')
    description_rol = models.TextField(blank=True, null=True, verbose_name='Descripción del Rol')
    photo = models.ImageField(upload_to='committee_members/', null=True, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    public = models.BooleanField(default=True, verbose_name='Publicado en landing')
    rol_esp = models.CharField(blank=True, null=True, max_length=500, verbose_name='Rol Español')
    description_rol_esp = models.TextField(blank=True, null=True, verbose_name='Descripción del Rol Español')

    def get_trans_rol(self):
        language = get_language()
        if language == 'es':
            return self.rol_esp or _(self.rol)
        else:
            return _(self.rol)

    def get_trans_description_rol(self):
        language = get_language()
        if language == 'es':
            return self.description_rol_esp or _(self.description_rol)
        else:
            return _(self.description_rol)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Committee Member'
        verbose_name_plural = 'Committee Members'
        ordering = ['name']


class TopicCategory(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Conferencia')
    icon = models.CharField(max_length=200, null=True, blank=True, verbose_name='Icono')
    name = models.CharField(blank=True, null=True, max_length=200, verbose_name='Nombre')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    public = models.BooleanField(default=True , verbose_name='Publicado en landing')
    name_esp = models.CharField(blank=True, null=True, max_length=200, verbose_name='Nombre Español')
    description_esp = models.TextField(blank=True, null=True, verbose_name='Descripción Español')

    def get_trans_name(self):
        language = get_language()
        if language == 'es':
            return self.name_esp or _(self.name)
        else:
            return _(self.name)

    def get_trans_description(self):
        language = get_language()
        if language == 'es':
            return self.description_esp or _(self.description)
        else:
            return _(self.description)

    def get_topics(self):
        return self.topics.filter(status=True, public=True)

    def get_topics_all(self):
        return self.topics.filter(status=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Topic Category'
        verbose_name_plural = 'Topic Categories'
        ordering = ['name']


class Topic(ModeloBase):
    category = models.ForeignKey(TopicCategory, related_name='topics', on_delete=models.CASCADE, verbose_name='Categoría')
    name = models.CharField(blank=True, null=True, max_length=200, verbose_name='Nombre')
    public = models.BooleanField(default=True, verbose_name='Publicado en landing')
    name_esp = models.CharField(blank=True, null=True, max_length=200, verbose_name='Nombre Español')

    def get_trans_name(self):
        language = get_language()
        if language == 'es':
            return self.name_esp or _(self.name)
        else:
            return _(self.name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['name']


class ScheduleConference(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Conferencia')
    order = models.IntegerField(blank=True, null=True, verbose_name='Orden')
    title = models.CharField(blank=True, null=True, max_length=200, verbose_name='Título')
    date_start = models.DateField(blank=True, null=True, verbose_name='Fecha de Inicio')
    date_end = models.DateField(blank=True, null=True, verbose_name='Fecha de Fin')
    date_str = models.CharField(blank=True, null=True, max_length=200, verbose_name='Fecha en Cadena')

    def get_trans_date_str(self):
        return _(self.date_str)

    def get_trans_title(self):
        return _(self.title)

    def get_details(self):
        return self.details.filter(status=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Schedule Conference'
        verbose_name_plural = 'Schedule Conferences'


class DetailScheduleConference(ModeloBase):
    cab = models.ForeignKey(ScheduleConference, related_name='details', on_delete=models.CASCADE, verbose_name='Cabecera')
    order = models.IntegerField(blank=True, null=True, verbose_name='Orden')
    title = models.CharField(blank=True, null=True, max_length=200, verbose_name='Título')
    time_start = models.TimeField(blank=True, null=True, verbose_name='Hora de Inicio')
    time_end = models.TimeField(blank=True, null=True, verbose_name='Hora de Fin')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    description_esp = models.TextField(blank=True, null=True, verbose_name='Descripción Español')

    def get_trans_title(self):
        return _(self.title)

    def get_trans_description(self):
        language = get_language()
        if language == 'es':
            return self.description_esp or _(self.description)
        else:
            return _(self.description)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Detail Schedule Conference'
        verbose_name_plural = 'Detail Schedule Conferences'
        ordering = ['order']


ROLES_FEE_CHOICE = (
    (1, _('Speaker')),
    (2, _('Attendees')),
    (3, _('Student')),
)


class ConferenceFee(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Conferencia')
    order = models.IntegerField(blank=True, null=True, verbose_name='Orden')
    role = models.IntegerField(default=1, choices=ROLES_FEE_CHOICE, verbose_name='Rol')
    value = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name='Valor')
    published = models.BooleanField(default=True, verbose_name='Publicado')

    def get_public(self):
        return 'text-success fa fa-check-circle' if self.published else 'text-danger fa fa-times-circle'

    def get_details(self):
        return self.details.filter(status=True).order_by('order')

    def get_value(self):
        return 'Free' if self.value == 0 else f"{self.value}"

    def __str__(self):
        return f'{self.get_role_display()} - {self.conference.__str__()}'

    class Meta:
        verbose_name = 'Conference Fee'
        verbose_name_plural = 'Conference Fees'
        ordering = ['order']


class DetailConferenceFee(ModeloBase):
    cab = models.ForeignKey(ConferenceFee, related_name='details', on_delete=models.CASCADE, verbose_name='Cabecera')
    order = models.IntegerField(blank=True, null=True, verbose_name='Orden')
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name='Descripción')

    def get_trans_description(self):
        return _(self.description)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Detail Conference Fee'
        verbose_name_plural = 'Detail Conference Fees'
        ordering = ['order']


class ImportantDates(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Conferencia')
    order = models.IntegerField(blank=True, null=True, verbose_name='Orden')
    icon = models.CharField(max_length=200, null=True, blank=True, verbose_name='Icono')
    title = models.CharField(blank=True, null=True, max_length=200, verbose_name='Titulo')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')

    def get_trans_title(self):
        return _(self.title)

    def get_trans_description(self):
        return _(self.description)

    def __str__(self):
        return f'{self.title} - {self.description}'

    class Meta:
        verbose_name = 'Important Date'
        verbose_name_plural = 'Important Dates'
        ordering = ['order']