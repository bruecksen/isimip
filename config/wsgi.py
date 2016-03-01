import os
from django.core.wsgi import get_wsgi_application

import environ

ROOT_DIR = environ.Path(__file__) -2
env = environ.Env()
env.read_env(ROOT_DIR('.env'))

if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production":
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
application = get_wsgi_application()

# if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production":
#     application = Sentry(application)
