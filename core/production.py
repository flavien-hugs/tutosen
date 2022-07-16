# core.production.py

from core.settings import *

# SECURITY WARNING: don't run with debug turned on in production
DEBUG = TEMPLATE_DEBUG = False

# https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'unstaschool.herokuapp.com',
    '*.herokuapp.com'
]

