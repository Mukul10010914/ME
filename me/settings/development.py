from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost']
SECRET_KEY = 'django-insecure-o2d1@avupx4$uoshtv7bil$@g%06&+t^e&qj^c3=hx@hv*#0wh'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'me',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}