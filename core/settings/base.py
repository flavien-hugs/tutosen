import re
import os
import logging.config
from pathlib import Path
from django.contrib.messages import constants as messages

from dotenv import dotenv_values

env = dotenv_values(".env")

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(os.path.dirname(abspath))
BASE_DIR = os.path.dirname(dirname)

SECRET_KEY = env.get("SECRET_KEY")

DEBUG = env.get("DEBUG")
TEMPLATE_DEBUG = DEBUG

META_KEYWORDS = ""
APPEND_SLASH = True
DEFAULT_CHARSET = "UTF-8"
SITE_DESCRIPTION = "Apprendre, Comprendre, Innover & Partager"

ALLOWED_HOSTS = ["*"]

SITE_NAME = "Bahut Forum Labs"
THOUSAND_SEPARATOR = " "
USE_THOUSAND_SEPARATOR = True
DEFAULT_CONTENT_TYPE = "text/html"

SITE_ID = 3
ADMIN_URL = "ssh-unsta/"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
]

THIRD_PARTY_APPS = [
    "django_summernote",
    "django.contrib.admin",
    "allauth",
    "allauth.account",
    "taggit",
    "widget_tweaks",
    "django_filters",
    "phonenumber_field",
    "phonenumbers",
    "compressor",
    "rest_framework",
    "corsheaders",
]

LOCALS_APPS = [
    "accounts.apps.AccountsConfig",
    "product.apps.ProductConfig",
    "boards.apps.BoardsConfig",
    "courses.apps.CoursesConfig",
    "blog.apps.BlogConfig",
    "comment.apps.CommentConfig",
    "pages.apps.PagesConfig",
    "api.apps.ApiConfig",
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCALS_APPS

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "utils.context_proc.tutosen_context_processor",
            ],
            "debug": DEBUG,
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

DEFAULT_HASHING_ALGORITHM = "sha1"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {"max_similarity": 0.9},
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 9},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


TIME_ZONE = "UTC"
LANGUAGE_CODE = "fr"

USE_TZ = False
USE_I18N = USE_L10N = True
DATE_INPUT_FORMATS = ("%d/%m/%Y", "%Y-%m-%d")


MEDIA_URL = "/media/"
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGOUT_URL = "home"
LOGIN_URL = "account_login"
ACCOUNT_LOGOUT_REDIRECT = "home"
ACCOUNT_ADAPTER = "accounts.adapter.CustomAccountAdapter"
LOGIN_REDIRECT_URL = ACCOUNT_ADAPTER

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USERNAME_VALIDATORS = False
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"
ACCOUNT_EMAIL_SUBJECT_PREFIX = f"{SITE_NAME} <no-reply@unsta.me>"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL


ACCOUNT_FORMS = {
    "signup": "accounts.forms.CustomSignupForm",
}

EMAIL_HOST = env.get("EMAIL_HOST")
EMAIL_PORT = env.get("EMAIL_PORT")
EMAIL_USE_TLS = env.get("EMAIL_USE_TLS")
EMAIL_HOST_USER = env.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = SERVER_EMAIL = "no-reply@unstainc.com"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

JET_THEMES = [{"theme": "light-gray", "color": "#222", "title": "Light Gray"}]

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "NATIONAL"

SUMMERNOTE_THEME = "bs4"

SUMMERNOTE_CONFIG = {
    "iframe": True,
    "summernote": {
        "airMode": False,
        "width": "1024",
        "height": "300",
        "toolbar": [
            [
                "font",
                [
                    "bold",
                    "italic",
                    "underline",
                    "clear",
                    "strikethrough",
                    "superscript",
                    "subscript",
                ],
            ],
            ["fontname", ["fontname"]],
            ["color", ["color"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["table", ["table"]],
            ["insert", ["link", "video"]],
            ["view", ["fullscreen", "codeview", "help"]],
        ],
        "attachment_absolute_uri": True,
        "attachment_require_authentication": True,
        "attachment_storage_class": "utils.function_utils.upload_image_path",
        "codemirror": {
            "mode": "htmlmixed",
            "lineNumbers": "true",
            "theme": "monokai",
        },
    },
}
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "http")
INTERNAL_IPS = ["localhost", "127.0.0.1", "127.0.0.1:8001", "127.0.0.1:8002"]


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}

CORS_ORIGIN_WHITELIST = (
    "http://localhost:8000",
    "htpp://localhost:8001",
    "htpp://localhost:8002"
)

TAGGIT_CASE_INSENSITIVE = True

IGNORABLE_404_URLS = [
    re.compile(r"^/cpc/"),
    re.compile(r"^/cpanel/"),
    re.compile(r"^/favicon\.ico$"),
    re.compile(r"^/robots\.txt$"),
    re.compile(r"\.(cgi|php|pl)$"),
    re.compile(r"^/apple-touch-icon.*\.png$"),
]

DISALLOWED_USER_AGENTS = [
    re.compile(r"^NaverBot.*"),
    re.compile(r"^EmailSiphon.*"),
    re.compile(r"^SiteSucker.*"),
    re.compile(r"^sohu-search"),
]


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
