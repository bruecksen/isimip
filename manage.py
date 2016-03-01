#!/usr/bin/env python
import os
import sys

import environ

ROOT_DIR = environ.Path(__file__) -1
APPS_DIR = ROOT_DIR.path('isi_mip')

env = environ.Env()
env.read_env(ROOT_DIR('.env'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
