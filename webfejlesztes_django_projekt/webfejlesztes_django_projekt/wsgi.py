"""
WSGI config for webfejlesztes_django_projekt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webfejlesztes_django_projekt.settings')

application = WhiteNoise(get_wsgi_application())
