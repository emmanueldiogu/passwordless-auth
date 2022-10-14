from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '.activepointsplus.com',
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q)tiu1*wvcn$x+=#&0vsm&(uc-zv*$)+1uuj&fz4m5wcf%_)f!'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''