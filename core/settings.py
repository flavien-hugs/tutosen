# core.settings.py

"""
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import re
import os
import logging.config
from pathlib import Path
from django.contrib.messages import constants as messages
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.getenv("DEBUG", "True"))
TEMPLATE_DEBUG = DEBUG

META_KEYWORDS = ''
DEFAULT_CHARSET = 'UTF-8'
SITE_DESCRIPTION = "Apprendre, Comprendre, Innover & Partager"

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1, localhost"
).split(",")

APPEND_SLASH = True
SITE_NAME = 'tutosen'
THOUSAND_SEPARATOR = ' '
USE_THOUSAND_SEPARATOR = True

SITE_ID = 3
ADMIN_URL = 'xx-tutosen/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'django.contrib.humanize',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'jet.dashboard',
    'jet',
    'django_summernote',
    'django.contrib.admin',

    'allauth',
    'allauth.account',

    'taggit',
    'widget_tweaks',
    'django_filters',
    'phonenumber_field',
    'phonenumbers',
    'compressor',

    'rest_framework',
    'corsheaders',
]

LOCALS_APPS = [
    'accounts.apps.AccountsConfig',
    'boards.apps.BoardsConfig',

    'courses.apps.CoursesConfig',
    'blog.apps.BlogConfig',
    'comment.apps.CommentConfig',
    'pages.apps.PagesConfig',

    'api.apps.ApiConfig',
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCALS_APPS

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.gzip.GZipMiddleware',

    # 'django.middleware.http.ConditionalGetMiddleware',
]

ROOT_URLCONF = 'core.urls'

# https://docs.djangoproject.com/en/dev/ref/settings/#templates
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
# https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
# https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
# https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types

TEMPLATE_DIR = str(BASE_DIR / 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",

                'utils.context_proc.tutosen_context_processor',
            ],

            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "SAMEORIGIN"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
            'PORT': 5432,
            'ATOMIC_REQUESTS': True
        }
    }

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.postgresql",
            'NAME': os.environ.get('DATABASE_NAME', 'tutosen'),
            'USER': os.environ.get('DATABASE_USER', 'tutosen'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'tutosen'),
            'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
            'PORT': os.environ.get('DATABASE_PORT', 5432),
            'ATOMIC_REQUESTS': True
        }
    }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3')
    }
}

# password hashers
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
# https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Hashage des donnees
# https://docs.djangoproject.com/fr/3.1/ref/settings/

DEFAULT_HASHING_ALGORITHM = 'sha1'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'max_similarity': 0.9}},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 9}
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# See: https://docs.djangoproject.com/en/3.2/ref/settings/#language-code
# See: https://docs.djangoproject.com/en/3.2/ref/settings/#use-i18n
# See: https://docs.djangoproject.com/en/3.2/ref/settings/#use-l10n
# See: https://docs.djangoproject.com/en/3.2/ref/settings/#use-tz

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'fr'
USE_I18N = USE_L10N = USE_TZ = True
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y-%m-%d')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# See: https://docs.djangoproject.com/en/3.2/ref/settings/#static-root

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# staticfiles finders
# See: https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#staticfiles-finders

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Les utilisateurs connectés sont redirigés ici s'ils
# consultent les pages de connexion/inscription

# https://docs.djangoproject.com/fr/dev/ref/settings/#logout-url
LOGOUT_URL = 'home'

# https://docs.djangoproject.com/fr/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'
ACCOUNT_LOGOUT_REDIRECT = 'home'

ACCOUNT_ADAPTER = "accounts.adapter.CustomAccountAdapter"

# https://docs.djangoproject.com/fr/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = ACCOUNT_ADAPTER

# Configuration django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USERNAME_VALIDATORS = False
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_SUBJECT_PREFIX = f"{SITE_NAME} <no-reply@tutosen.com>"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL

# Control the forms that django-allauth uses

ACCOUNT_FORMS = {
    "signup": "accounts.forms.CustomSignupForm",
}

EMAIL_PORT = 587
EMAIL_TIMEOUT = 5
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_HOST_USER = 'flavienhgs@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'hello@tutosen.com'

# Pour le développement, envoyer tous les courriers électroniques
# à la console au lieu de les envoyer

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend',
)

# Activez le backend de stockage WhiteNoise qui se charge de compresser
# les fichiers statiques et de créer des noms uniques pour chaque version
# afin qu'ils puissent être mis en cache à jamais en toute sécurité.

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# django/core/serializers/json.Serializer pour avoir la fonction de `dumps`.

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


# https://docs.djangoproject.com/fr/3.2/ref/settings/#message-tags
# Messages built-in framework

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Configuration django-jet
# https://jet.readthedocs.io/en/latest/config_file.html

JET_THEMES = [
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "NATIONAL"

# Summernote configuration
# https://github.com/summernote/django-summernote

# Show summernote with Bootstrap4
SUMMERNOTE_THEME = 'bs4'

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode, default
    'iframe': True,

    'summernote': {
        # As an example, using Summernote Air-mode
        'airMode': False,

        # Change editor size
        'width': '100%',
        'height': '300',

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        'toolbar': [
            ['font', ['bold', 'italic', 'underline', 'clear', 'strikethrough', 'superscript', 'subscript']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],

        # Set to `True` to return attachment paths in absolute URIs.
        'attachment_absolute_uri': True,

        # Require users to be authenticated for uploading attachments.
        'attachment_require_authentication': True,

        # Set custom storage class for attachments.
        'attachment_storage_class': 'utils.function_utils.upload_image_path',

        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            # You have to include theme file in 'css' or 'css_for_inplace' before using it.
            'theme': 'monokai',
        },
    },
}

# config django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
INTERNAL_IPS = ['localhost', '127.0.0.1', '127.0.0.1:8001', '127.0.0.1:8002']

# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'htpp://localhost:8001',
    'htpp://localhost:8002',
    'https://tutosen.unsta.net'
)

# https://django-taggit.readthedocs.io/en/latest/getting_started.html

TAGGIT_CASE_INSENSITIVE = True

# https://docs.djangoproject.com/fr/3.2/ref/settings/#ignorable-404-urls

IGNORABLE_404_URLS = [
    re.compile(r'^/cpc/'),
    re.compile(r'^/cpanel/'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
    re.compile(r'\.(cgi|php|pl)$'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
]

DISALLOWED_USER_AGENTS = [
    re.compile(r'^NaverBot.*'),
    re.compile(r'^EmailSiphon.*'),
    re.compile(r'^SiteSucker.*'),
    re.compile(r'^sohu-search'),
]


# Django-compressor config
# https://django-compressor.readthedocs.io/en/stable/settings/#settings

COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_OUTPUT_DIR = "cache"
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_REBUILD_TIMEOUT = 5400
COMPRESS_PRECOMPILERS = (
    ("text/less", "/usr/local/bin/lessc {infile} {outfile}"),
    ("text/x-sass", "/usr/local/bin/sass {infile} {outfile}"),
    ("text/x-scss", "/usr/local/bin/sass {infile} {outfile}"),
)
COMPRESS_OFFLINE_CONTEXT = {
    "STATIC_URL": "STATIC_URL",
}
