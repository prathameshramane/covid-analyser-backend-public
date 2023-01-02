from .base import *

APP_URL = ""
HOST_URL = ""

DEBUG = True

ALLOWED_HOSTS = ["*"]


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# CORS

CORS_ALLOW_ALL_ORIGINS = True