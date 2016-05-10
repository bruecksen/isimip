#!/bin/bash

#sudo drop db
psql -c 'drop database "isi-mip"'
psql -c 'create database "isi-mip"'
psql -c 'grant all on database "isi-mip" to nutz'

python manage.py migrate || exit 1

echo "from django.contrib.auth.models import User; User.objects.create_superuser('nuts', 's@noova.de', 'tux');User.objects.create_superuser('matthias.brueck', 'mb@sinnwerkstatt.com', 'tux');User.objects.create_superuser('lila.warszawski', 'lila@noova.de', 'tux')" | python manage.py shell 2>/dev/null

