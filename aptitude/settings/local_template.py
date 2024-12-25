from .base import *
import os
import socket
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# FORCE_SCRIPT_NAME = '/api'

ALLOWED_HOSTS = ['localhost']

SITE_URL = 'http://localhost:8000/api/'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASE_DIR = Path(BASE_DIR) / 'db'

print(DATABASE_DIR)

DATABASES = {
    'es': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'aptitude.db'),
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_DIR / 'aptitude.db',
    },
    'cat': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'cat_aptitude.db'),
    }
}

DATABASE_ROUTERS = ['aptitude.settings.databases.DatabaseRouter']

MIDDLEWARE += ['aptitude.settings.databases.RouterMiddleware']

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory to store media files

# If the host name starts with 'live', DJANGO_HOST = "production"
DJANGO_HOST = socket.gethostname()

print(DJANGO_HOST)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'EMAIL_HOST'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
DEFAULT_FROM_EMAIL = "DEFAULT_FROM_EMAIL"
SERVER_EMAIL = "SERVER_EMAIL"

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = False # Automatically log the user in.

ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = False
REGISTRATION_USE_SITE_EMAIL = False
REGISTRATION_SITE_USER_EMAIL = "info"
REGISTRATION_DEFAULT_FROM_EMAIL = "info@aptitude.com"
REGISTRATION_EMAIL_HTML = True

def reg_admins(*args, **kwargs):
    print("=================================")
    print(args, kwargs)
    print("=================================")
    return [('Admin', 'admin@admin.com'), ]

REGISTRATION_ADMINS = 'aptitude.settings.local.reg_admins' # [('Alberto Labarga', 'alberto.labarga@gmail.com'), ]
