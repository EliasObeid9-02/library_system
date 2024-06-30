from os import environ
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

from rest_framework.settings import api_settings

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

STATIC_URL = "static/"

load_dotenv(PROJECT_DIR / ".eVar" / ".env")

SECRET_KEY = environ.get("SECRET_KEY")
DEBUG = True if environ.get("DEBUG") == "True" else False

ALLOWED_HOSTS = [
    "library-system.local",
]

INSTALLED_APPS = [
    # custom apps
    "user_auth",
    "library_system",
    # external apps
    "django_extensions",
    "django_filters",
    "rest_framework",
    "knox",
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(days=7),
    "USER_SERIALIZER": "user_auth.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": None,
    "AUTO_REFRESH": False,
    "EXPIRY_DATETIME_FORMAT": api_settings.DATETIME_FORMAT,
}

DATABASES = {
    "dev": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": environ.get("DB_NAME"),
        "USER": environ.get("DB_USER"),
        "PASSWORD": environ.get("DB_PASS"),
        "HOST": environ.get("DB_HOST"),
        "PORT": environ.get("DB_PORT"),
    },
    "prod": {},
}
DATABASES["default"] = DATABASES["dev"] if DEBUG else DATABASES["prod"]

AUTH_USER_MODEL = "user_auth.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WSGI_APPLICATION = "core.wsgi.application"

ROOT_URLCONF = "core.urls"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
