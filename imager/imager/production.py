from settings import *
import os

SITE_URL = 'http://imager.joelstanner.com'
DEBUG = False
TEMPLATE_DEBUG = False
THUMBNAIL_DEBUG = False
ALLOWED_HOSTS = ['.joelstanner.com',
                 '192.168.99.100',
                 '159.203.75.183']
SECRET_KEY = os.environ['SECRET_KEY']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
PASSWORD_HASHERS = ('django.contrib.auth.hashers.PBKDF2PasswordHasher',
                    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
                    'django.contrib.auth.hashers.BCryptPasswordHasher',
                    'django.contrib.auth.hashers.SHA1PasswordHasher',
                    'django.contrib.auth.hashers.MD5PasswordHasher',
                    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
                    'django.contrib.auth.hashers.CryptPasswordHasher')
