"""
WSGI config for kanga project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/


import os
import django.contrib.auth
import django.core.handlers.wsgi

os.environ["DJANGO_SETTINGS_MODULE"] = "kanga.settings"
application = django.core.handlers.wsgi.WSGIHandler()

django.contrib.auth.REDIRECT_FIELD_NAME = 'return_uri'
# SITE_URL = 'http://kanga.sec.samsung.net'
"""
import os
import sys
#import django.contrib.auth
from django.core.wsgi import get_wsgi_application
# from dj_static import Cling

sys.path.append('c:/kanga/sw/KangaIDE')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanga.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "kanga.settings"
application = get_wsgi_application()

# django.contrib.auth.REDIRECT_FIELD_NAME = 'return_uri'