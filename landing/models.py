from django.db import models
from core.custom_models import ModeloBase


# Create your models here.

class Conference(ModeloBase):
    title = models.CharField(max_length=200, verbose_name='Título')
    subtitle = models.CharField(max_length=200, verbose_name='Subtítulo')
    start_date = models.DateField(verbose_name='Fecha de Inicio')
    end_date = models.DateField(verbose_name='Fecha de Fin')
    date_str = models.CharField(max_length=200, verbose_name='Fecha')
    location_str = models.CharField(max_length=200, verbose_name='Ubicación')
    image_princial = models.ImageField(upload_to='conference/images/', verbose_name='Imagen Principal')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def get_summary(self):
        return self.summary_set.filter(status=True, activo=True, public=True).order_by('-id').first()

    def get_topics(self):
        return self.topiccategory_set.filter(public=True, status=True)

    def get_active(self):
        return 'text-success fa fa-check-circle' if self.active else 'text-danger fa fa-times-circle'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Conference'
        verbose_name_plural = 'Conferences'


class ItemDetailConference(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    principal_text = models.CharField(verbose_name='Texto Principal')
    secondary_text = models.CharField(verbose_name='Texto Secundario')
    color = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name=u"Color")

    def __str__(self):
        return f'{self.principal_text} - {self.secondary_text}'

    class Meta:
        verbose_name = 'Item Detail Conference'
        verbose_name_plural = 'Item Detail Conferences'


class PhotoCatalogConference(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='conference/catalog/', verbose_name='Imagen')
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Photo Catalog Conference'
        verbose_name_plural = 'Photo Catalog Conferences'


class LandingConfereceCarousel(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to='landing_conference_carousel/')
    public = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.conference.title} - {self.order}'


class CommitteeCategory(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0, null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name='Activo')
    public = models.BooleanField(default=True, verbose_name='Publicado en landing')

    def get_members_all(self):
        return self.members.filter(status=True)

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
    order = models.IntegerField(default=0)
    category = models.ForeignKey(CommitteeCategory, related_name='members', on_delete=models.CASCADE)
    sexo = models.CharField(verbose_name="Sexo", max_length=50, choices=SEXO, default="NINGUNO",  null=True, blank=True)
    name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    rol = models.CharField(max_length=500, default='')
    description_rol = models.TextField(default='')
    photo = models.ImageField(upload_to='committee_members/', null=True, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    public = models.BooleanField(default=True, verbose_name='Publicado en landing')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Committee Member'
        verbose_name_plural = 'Committee Members'
        ordering = ['name']


class TopicCategory(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=True)

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
    category = models.ForeignKey(TopicCategory, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['name']


class ScheduleConference(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=200, verbose_name='Título')
    date_start = models.DateField(verbose_name='Fecha de Inicio')
    date_end = models.DateField(verbose_name='Fecha de Fin')
    date_str = models.CharField(max_length=200, verbose_name='Fecha')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Schedule Conference'
        verbose_name_plural = 'Schedule Conferences'


class DetailScheduleConference(ModeloBase):
    cab = models.ForeignKey(ScheduleConference, related_name='details', on_delete=models.CASCADE, verbose_name='Cabecera')
    order = models.IntegerField(default=0, verbose_name='Orden')
    title = models.CharField(max_length=200, verbose_name='Título')
    time_start = models.TimeField(verbose_name='Hora de Inicio')
    time_end = models.TimeField(verbose_name='Hora de Fin')
    description = models.TextField(verbose_name='Descripción')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Detail Schedule Conference'
        verbose_name_plural = 'Detail Schedule Conferences'
        ordering = ['order']


ROLES_FEE_CHOICE = (
    (1, 'Speaker'),
    (2, 'Attendees'),
    (3, 'Student'),
)


class ConferenceFee(ModeloBase):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name='Orden')
    role = models.IntegerField(choices=ROLES_FEE_CHOICE, verbose_name='Rol')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
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
    order = models.IntegerField(default=0, verbose_name='Orden')
    description = models.CharField(max_length=200, verbose_name='Descripción')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Detail Conference Fee'
        verbose_name_plural = 'Detail Conference Fees'
        ordering = ['order']

