# core.settings.py

"""
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

__author__ = 'Flavien-hugs <flavienhgs@pm.me>'
__version__ = 'V.0.0.1'
__copyright__ = '© 2021 unsta'

from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = config('DEBUG', default=True, cast=bool)

META_KEYWORDS = ''
DEFAULT_CHARSET = 'UTF-8'
SITE_DESCRIPTION = "Apprendre, Comprendre, Innover & Partager"
DEFAULT_CONTENT_TYPE = 'text/html'

ALLOWED_HOSTS = []
APPEND_SLASH = True
SITE_NAME = 'tutosen'
THOUSAND_SEPARATOR = ' '
USE_THOUSAND_SEPARATOR = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'django.contrib.sitemaps',
]

PACKAGES_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'tinymce',
    'phonenumber_field',
    'phonenumbers',
]

LOCALS_APPS = [
    'accounts.apps.AccountsConfig',
    'boards.apps.BoardsConfig',
    'courses.apps.CoursesConfig',
    'pages.apps.PagesConfig',
]

INSTALLED_APPS += PACKAGES_APPS + LOCALS_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'utils.context_proc.tutosen_context_processor',
            ],

            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
            'OPTIONS': {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'max_similarity': 0.9,}},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 9,}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# password hashers
# https://docs.djangoproject.com/fr/3.1/topics/auth/passwords/

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Hashage des donnees
# https://docs.djangoproject.com/fr/3.1/ref/settings/

DEFAULT_HASHING_ALGORITHM = 'sha1'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'fr-fr'
USE_I18N = USE_L10N = USE_TZ = True
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y-%m-%d')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']


# staticfiles finders
# See: https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#staticfiles-finders

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Activez le backend de stockage WhiteNoise qui se charge de compresser
# les fichiers statiques et de créer des noms uniques pour chaque version
# afin qu'ils puissent être mis en cache à jamais en toute sécurité.

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# django/core/serializers/json.Serializer pour avoir la fonction de `dumps`.

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Configuration django-jet
# https://jet.readthedocs.io/en/latest/config_file.html

JET_THEMES = [
    {
        'theme': 'default',
        'color': '#47bac1',
        'title': 'Default'
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

# configuration tinymce
# https://django-tinymce.readthedocs.io/en/latest/installation.html#configuration

TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,",
    'toolbar': '''
        fullscreen preview bold italic underline | fontselect,
        fontsizeselect | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample |
    ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}
