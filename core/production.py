# core.production.py

import dj_database_url
from core.settings import *

# SECURITY WARNING: don't run with debug turned on in production

DEBUG = TEMPLATE_DEBUG = False

# https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts

ALLOWED_HOSTS = [
    'unstaschool.herokuapp.com',
    '*.herokuapp.com'
]

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

# https://docs.djangoproject.com/fr/3.0/ref/settings/
# Let's Encrypt ssl/tls https

X_FRAME_OPTIONS = "DENY"
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
