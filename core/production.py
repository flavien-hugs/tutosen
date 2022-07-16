# core.production.py

from core.settings import *
import dj_database_url


# SECURITY WARNING: don't run with debug turned on in production
DEBUG = TEMPLATE_DEBUG = False

# https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'unstaschool.herokuapp.com',
    '*.herokuapp.com'
]

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)
