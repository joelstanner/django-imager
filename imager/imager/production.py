from settings import DEBUG, TEMPLATE_DEBUG, ALLOWED_HOSTS, STATIC_ROOT, BASE_DIR
import os

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['http://ec2-54-148-71-55.us-west-2.compute.amazonaws.com', 'localhost']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
