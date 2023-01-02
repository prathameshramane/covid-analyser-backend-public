from .base import *

APP_URL = "<APP URL HERE>"
HOST_URL = "<HOST URL HERE>"

DEBUG = False

ALLOWED_HOSTS = [
    "<ALLOWED HOST HERE>",
]


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# CORS

CORS_ALLOW_ALL_ORIGINS = True