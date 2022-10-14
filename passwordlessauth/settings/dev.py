from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q)tiu1*wvcn$x+=#&0vsm&(uc-zv*$)+1uuj&fz4m5wcf%_)f!'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'emmanueldiogu@gmail.com'
EMAIL_HOST_PASSWORD = 'ukqvwotnwnqwbags'
DEFAULT_FROM_EMAIL = 'noreply@activepointsplus.com'