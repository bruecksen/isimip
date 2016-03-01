# -*- coding: utf-8 -*-
'''
Production Configurations

- Use djangosecure
- Use mailgun to send emails
- Use Redis on Heroku

- Use sentry for error logging


'''
from __future__ import absolute_import, unicode_literals

import logging


from .common import *  # noqa


SECRET_KEY = env("DJANGO_SECRET_KEY")

EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

# django-secure
# ------------------------------------------------------------------------------
# INSTALLED_APPS += ("djangosecure", )
# raven sentry client
# See https://docs.getsentry.com/hosted/clients/python/integrations/django/
# INSTALLED_APPS += ('raven.contrib.django.raven_compat', )
# SECURITY_MIDDLEWARE = (
# #     'djangosecure.middleware.SecurityMiddleware',
# )
# RAVEN_MIDDLEWARE = ('raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
#                     'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',)
# MIDDLEWARE_CLASSES = SECURITY_MIDDLEWARE + \
#     RAVEN_MIDDLEWARE + MIDDLEWARE_CLASSES
#

INSTALLED_APPS += ("gunicorn", )

DATABASES['default'] = env.db("DATABASE_URL")

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['isi-mip.net'])

