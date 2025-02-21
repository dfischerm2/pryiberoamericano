import os
from pathlib import Path

# from django.conf.global_settings import CACHES

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["*"]

WKHTMLTOPDF_DEBUG = True
# SESSION CONFIGURATION
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 28800

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465

# CREDENCIALES
import json

with open(os.path.join(BASE_DIR, 'credenciales.json')) as json_file:
    data = json.load(json_file)
    # POSTGRES
    POSTGRES_PASSWORD = data['POSTGRES_PASSWORD']
    POSTGRES_HOST = data['POSTGRES_HOST']
    POSTGRES_PORT = data['POSTGRES_PORT']
    POSTGRES_DBNAME = data['POSTGRES_DBNAME']
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = data['SECRET_KEY']
    EMAIL_HOST_USER = data['EMAIL_HOST_USER']
    DEFAULT_FROM_EMAIL = data['DEFAULT_FROM_EMAIL']
    EMAIL_HOST_PASSWORD = data['EMAIL_HOST_PASSWORD']
    SENDGRID_API_KEY = data['SENDGRID_API_KEY']
    # WKHTMLTOPDF
    WKHTMLTOPDF_CMD = data['WKHTMLTOPDF_CMD']
    # SSL
    USE_SSL = data['USE_SSL']
    SECURE_SSL_REDIRECT = USE_SSL
    DEBUG = data["DEBUG"]
    DOMINIO_GENERAL = data["DOMINIO_GENERAL"]
    WINDOWS = data["WINDOWS"]
    URL_GENERAL = ("https://" if USE_SSL else "http://") + DOMINIO_GENERAL
    ADMINS = data["ADMINS"]
    CACHES_REDIS = data.get("CACHES_REDIS")
    ID_GRUPO_USUARIO = data["ID_GRUPO_USUARIO"]

# CONFIGURACIONES

WKHTMLTOPDF_CMD_OPTIONS = {'encoding': 'utf8', 'quiet': True, 'enable-local-file-access': True}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # LOCAL APPS
    'autenticacion.apps.AutenticacionConfig',
    'seguridad.apps.SeguridadConfig',
    'area_geografica.apps.AreaGeograficaConfig',
    'public.apps.PublicConfig',
    'financiero.apps.FinancieroConfig',
    'pedidos.apps.PedidosConfig',
    # packages
    'wkhtmltopdf',
    'django_select2',
    'form_utils',
    'landing',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Middleware necesario para cambiar idioma}
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # custom middlewares
    'core.custom_middleware.InitialDataApp',
]

ROOT_URLCONF = 'pryiberoamericano.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'landing/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pryiberoamericano.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_DBNAME,
        'USER': 'postgres',
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
        'ATOMIC_REQUESTS': True,
    },

}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# caches redis django-select2
# if CACHES_REDIS:
#     CACHES["django-select2"] = {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
#     SELECT2_CACHE_BACKEND = 'django-select2'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LOGIN_URL = '/autenticacion/login/'

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('es', 'Spanish'),
    ('en', 'English'),
)

AUTH_USER_MODEL = "autenticacion.Usuario"

STATIC_URL = '/static/'
STATIC_ROOT = ''

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'  # If you wish to delay updates to your test suite
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SITE_STORAGE = Path(BASE_DIR)
LOGIN_URL = '/login/'

FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    'https://iberoamericano.sageformoodle.ec',
    'https://iberoamericano.sageformoodle.ec',
    'https://www.iberoamericano.sageformoodle.ec',
    'http://127.0.0.1:8080',
    'http://127.0.0.1',
    'http://localhost:8000',
    'http://localhost:8080',
    'http://localhost',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    'https://iberoamericano.sageformoodle.ec',
    'https://www.iberoamericano.sageformoodle.ec',
]

CORS_ORIGIN_WHITELIST = [
    'https://iberoamericano.sageformoodle.ec',
    'https://www.iberoamericano.sageformoodle.ec',
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CSRF_TRUSTED_ORIGINS = [
    'https://iberoamericano.sageformoodle.ec',
    'https://www.iberoamericano.sageformoodle.ec',
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True