"""
Django settings for tutorial project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+=af&a1=-iesqg8wxnwz*a&3ehhpw%rdwu5z%tmu^f)rc6m24$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'app01',
    'api',
    'app02',
    'covid_ksh_demo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tutorial.urls'

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

WSGI_APPLICATION = 'tutorial.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        # ?????????????????????
        'ENGINE': 'django.db.backends.mysql',
        # ??????????????????
        'NAME': 'learn_drf',
        # ?????????????????????IP????????????????????????localhost???127.0.0.1???
        'HOST': '127.0.0.1',
        # ??????MySQL??????????????????
        'PORT': 3307,
        # ???????????????????????????
        'USER': 'root',
        'PASSWORD': 'iflytek',
        # ???????????????????????????
        'CHARSET': 'utf8',
        # ????????????????????????????????????
        'TIME_ZONE': 'Asia/Shanghai',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# html?????????????????????????????????????????????????????? ???STATICFILES_DIRS???
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

REST_FRAMEWORK = {
    # "DEFAULT_AUTHENTICATION_CLASSES": ['utils.auth.Authentication', ],
    # "DEFAULT_PERMISSION_CLASSES": ["utils.auth.SvipPermission"],
    # "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_THROTTLE_CLASSES": ["api.utils.auth.UserThrottle"],
    "DEFAULT_THROTTLE_RATES": {
        "Liuzhu": "5/min",
        "LiuzhuUser": "10/min"
    },
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "VERSION_PARAM": "version",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser", "rest_framework.parsers.FormParser"],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# celery
import djcelery

djcelery.setup_loader()  # ??????

BROKER_URL = "redis://127.0.0.1:6379/2"  # ?????????????????????
CELERY_IMPORTS = ("CeleryTask.task")  # ??????
CELERY_TIMEZONE = "Asia/Shanghai"  # ??????
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# ????????????
from celery.schedules import timedelta, crontab

# python manage.py celery worker --loglevel ??????workder
# python manage.py celery beat --loglevel ??????????????????

CELERYBEAT_SCHEDULE = {
    u'??????????????????': {
        'task': "CeleryTask.task.start_get_data",
        "schedule": timedelta(seconds=30)
    }
}
