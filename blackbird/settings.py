"""
Django settings for blackbird project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/


For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4-rcjw!ex+vkh2t#etm1y!vbza)&!p*9b8p43wnzg(sn8s-965'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['bluecrow2-env.us-east-2.elasticbeanstalk.com', 'localhost']

# More security settings

SECURE_BROWSER_XSS_FILTER=True

# SECURE_SSL_REDIRECT=True

SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS='DENY'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #This is for the app I've created.
    'eggs.apps.EggsConfig',
    # 'celery.contrib.testing.tasks'
]
# this is good for celery
CELERY_TASK_ALWAYS_EAGER=True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blackbird.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'blackbird.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
        }
    }
else :
    DATABASES = { 
        'default':{
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'cardinal',
            'USER': 'gamel',
            'PORT':5433,
            'PASSWORD':'abba',
            'HOST':'localhost',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# added 

CSRF_COOKIE_SECURE=False

SESSION_COOKIE_SECURE=False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
#location on particular machine
# linuxLocation = "/mnt/LinuxLanzaProject/" 44
#two different static files was highly confusing! this has been changed so they are all the same. 
STATIC_ROOT= 'eggs/static/'

#This is where uploaded files will be stored. 
MEDIA_ROOT = "aviary/"

# FILE_UPLOAD_MAX_MEMORY_SIZE = 2
# This is who email erorr messages are sent to when DEBUG is false

ADMINS = [('Gabriel', 'gameltzer@gmail.com')]


SERVER_EMAIL = 'scrubjay065@gmail.com'
DEFAULT_FROM_EMAIL = 'scrubjay065@gmail.com'
# 
# this is configuring the SMTP server. Change this to environment variables later. 


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'scrubjay065@gmail.com'
EMAIL_HOST_PASSWORD = 'd2a389#5'

# this is recommended here: http://blog.appliedinformaticsinc.com/how-to-setup-the-django-error-reporting-mail-admins/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(module)s %(message)s'
        },
    },
    'handlers' :{
        'console':{
            'class':'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,

        }
    },
    'loggers':{
        'django': {
            'handlers': ['mail_admins','console'],
            'propagate':True,
            'level': 'DEBUG',
        },
    }
}

DEBUG_PROPAGATE_EXCEPTIONS=False


     