from settings import *
import os

DEBUG = False
TEMPLATE_DEBUG = False
THUMBNAIL_DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ['SECRET_KEY']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
