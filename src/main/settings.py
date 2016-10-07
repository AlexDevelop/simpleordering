"""
Django settings for src project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Define the project (src) root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Repository root, can be used to determine 'non-code' paths such as logs
REPOSITORY_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bn!-_hi&+b45q$a@wj0#(beqdl7s*^ms&x04+#64-8=6&!dxvn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = (
    # Django CMS custimization
    'suit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'rest_framework',
    'bootstrap3',
    'bootstrap3_datetime',

    # Custom
    'order',
    'frontend',
    'authtoken',
    'translation_manager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/api/orders/'

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'


TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': dict(),
    }
}

# ######################## Locale and Languages settings ######################## #

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nl-NL'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LOCALE_PATHS = (
    PROJECT_ROOT + '/locale',
)

LANGUAGES = (
    ('nl', _(u'Nederlands')),
    ('en', _(u'English')),
)


# ######################## End Locale and Languages settings ######################## #


# ######################## Statics and Media files settings ######################## #

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = REPOSITORY_ROOT + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = REPOSITORY_ROOT + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'main', 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'main', 'templates'),
        ],
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

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    # os.path.join(REPOSITORY_ROOT, '../../templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# ######################## End Statics and Media files settings ######################## #

# Django Suit configuration
SUIT_CONFIG = {
    'ADMIN_NAME': 'Ordering AlmereAutomatisering',
}

# ######################## REST Framework API Settings ######################## #
# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#         'rest_framework.permissions.AllowAny',
#     ]
# }

REST_FRAMEWORK_RENDERERS = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

# Settings for django-bootstrap3
BOOTSTRAP3 = {
    'set_required': False,
    'error_css_class': 'bootstrap3-error',
    'required_css_class': 'bootstrap3-required',
    'javascript_in_head': True,
}

PORT = '8000'

# DSL Order parameters
EVENT_VALIDATION_V7 = '%2FwEWCALJ%2BduGDwLU4YLJCwLsu%2BfPCQL2soCpDQKJ%2BpbDCgLo1KSVDwKE%2FfOFAgLO4PZGBs2n3KWC%2BoGKuyIOeytm4GX4Yyc%3D'
VIEW_STATE_V7 = '2FwEPDwULLTExNjY2MDU5OTEPZBYCAgMPZBYCAgEPFgIeCWlubmVyaHRtbAUdVmVyc2lvbiA3LjEsIFdlZCAzMCBNYXIgMjA6MTRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBQlTaG93RGVidWcFGENoZWNrZm9yVXBncmFkZURvd25HcmFkZRDTZ1FztBXrKn4JDzgTyyOZh%2FLN'
VIEW_STATE_GEN_V7 = 'D8B62B3A'

EVENT_VALIDATION_V8 = '%2FwEWCwKT47RRAtThgskLAuy7588JAvaygKkNAon6lsMKAqXAvLcJAujUpJUPAvbzlNYLArnAvtIGApWklc4GAs7g9kYOSolULdpXtXhzkRoH0URxVAjleA%3D%3D'
VIEW_STATE_V8 = '%2FwEPDwUKMTY5MDMxMTI0OA9kFgICAw9kFgYCAQ8WAh4JaW5uZXJodG1sBR1WZXJzaW9uIDguMCwgVGh1IDI5IFNlcCAxNjowNmQCIw8QDxYCHgdDaGVja2VkaGRkZGQCJQ8QDxYCHwFnZGRkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBgUJU2hvd0RlYnVnBQ1Db3ZlcmFnZUNoZWNrBQ1Db3ZlcmFnZUNoZWNrBQZDb3BwZXIFBUZpYmVyBQVGaWJlcp69wAlEhiUEQF%2BXNV0UM6DeDmVV'
VIEW_STATE_GEN_V8 = 'B1924A1F'

try:
    from main.params import *
except ImportError:
    pass