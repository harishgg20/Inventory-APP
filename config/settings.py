import os
from pathlib import Path
from dotenv import load_dotenv
from .jazzmin import JAZZMIN_SETTINGS

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
DEBUG = os.getenv('DEBUG', '1') == '1'
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'inventory_app',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'inventory_app' / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'

if os.getenv('USE_SQLITE') == '1':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'inventory'),
            'USER': os.getenv('POSTGRES_USER', 'inventory_user'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'strongpassword'),
            'HOST': os.getenv('POSTGRES_HOST', 'db'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'inventory_app' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost,http://127.0.0.1').split(',')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_BACKEND', 'redis://redis:6379/0')

# If we are using SQLite (Local/Debug), we likely don't have Redis running.
# Use Synchronous execution to avoid timeouts.
if os.getenv('USE_SQLITE') == '1':
    CELERY_TASK_ALWAYS_EAGER = True

# Celery Beat (Periodic Tasks)
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'check-low-stock-every-30-mins': {
        'task': 'inventory_app.tasks.check_low_stock_and_alert',
        'schedule': 1800.0, # 30 minutes
    },
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
