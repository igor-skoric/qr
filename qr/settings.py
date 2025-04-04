"""
Django settings for qr project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api

from pathlib import Path
import os
import dj_database_url
import environ

# Inicijalizacija
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)
print(DEBUG)
ALLOWED_HOSTS = ['testqrcode.rs.itbranch.rs', '127.0.0.1', 'qr-codes-1d661a844374.herokuapp.com','localhost']

CSRF_TRUSTED_ORIGINS = [
    'https://qr-codes-1d661a844374.herokuapp.com',  # Replace with your Heroku domain
    'http://localhost:8000',  # Optionally add localhost for local development
    'http://127.0.0.1:8000',  # Optionally add localhost for local development
    'http://localhost:8000'
]

# Application definition

INSTALLED_APPS = [

    'website',

    # Aplikacije za kanale (WebSocket)
    'daphne',
    'channels',

    # Aplikacije za frontend, teme, i administraciju
    'tailwind',
    # Dodatne aplikacije
    'django_browser_reload',
    'theme',
    'jazzmin',
    # Osnovne Django aplikacije
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Aplikacije za medijske fajlove - OBAVEZNO DA BUDU ISPOD
    'cloudinary',
    'cloudinary_storage',

]


ADMIN_SITE = 'qr.admin.admin_site.admin_site'

SITE_ID = 1

ASGI_APPLICATION = "qr.asgi.application"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # Za lokalni razvoj
    },
}

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'qr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.default_client'
            ],
        },
    },
]

# Konfiguracija Cloudinary-ja
cloudinary.config(
    cloud_name=env("CLOUDINARY_CLOUD_NAME"),
    api_key=env("CLOUDINARY_API_KEY"),
    api_secret=env("CLOUDINARY_API_SECRET"),
    secure=True
)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
    "SECURE": True,
    'DEFAULT_TRANSFORMATION': [
        {'quality': 'auto'},  # Automatska optimizacija kvaliteta
        {'fetch_format': 'auto'},  # Automatski format slike (npr. WebP umesto PNG)
    ]
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': dj_database_url.config(default=env("DATABASE_URL"))
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Europe/Belgrade'


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Putanja gde će se statički fajlovi čuvati u produkciji (nakon komande collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Direktori za dodatne statičke fajlove
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Direktori za medijske fajlove
# MEDIA_URL = '/media/'
MEDIA_URL = 'https://res.cloudinary.com/dxzcabe8c/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tailwind CSS
TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


LOGGING_DIR = os.path.join(BASE_DIR, "logs")  # Kreiraj folder za logove
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

# LOGOVI
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "error": {
            "format": "{levelname} {asctime} {pathname}:{lineno} {message}",
            "style": "{",
        },
    },
    "handlers": {
        # Handler za ERROR logove
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "errors.log"),
            "maxBytes": 5 * 1024 * 1024,  # 5MB po fajlu
            "backupCount": 3,  # Čuva poslednja 3 log fajla
            "formatter": "error",
        },
        # Handler za INFO logove
        "info_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "info.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["error_file", "info_file"],
            "level": "INFO",  # Hvatamo i INFO i ERROR logove
            "propagate": True,
        },
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "My Admin Panel",
    "site_header": "My Admin Panel",
    "welcome_sign": "Welcome to My Admin Panel",
    "custom_links": {
        "website": [{
            "name": "Home",
            "url": "/",
            "icon": "fas fa-home",
            "permissions": ["auth.view_user"]
        }]
    },
}
