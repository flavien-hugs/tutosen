# locanto.production.py

from core.settings import *

# SECURITY WARNING: don't run with debug turned on in production
PREPEND_WWW = True
DEBUG = TEMPLATE_DEBUG = False

# https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
]


# APPLICATION DEFINITION

INSTALLED_APPS += ['whitenoise.runserver_nostatic']

# 'django.middleware.security.SecurityMiddleware',
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware',]

# https://docs.djangoproject.com/fr/3.0/ref/settings/
# Let's Encrypt ssl/tls https

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CSRF_USE_SESSIONS = True
CSRF_COOKIE_SECURE = True
# CSRF_FAILURE_VIEW = ''

# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR / "logs/debug.log",
            "when": "D",
            "interval": 1,
            "backupCount": 100,
        }
    },

    'loggers': {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },

        "project": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },

        "": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
    },
}
