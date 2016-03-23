#!/bin/bash

#sudo drop db
sudo psql -c 'drop database "isi-mip"'
sudo psql -c 'create database "isi-mip"'
sudo psql -c 'grant all on database "isi-mip" to nutz'

python manage.py migrate && echo "from django.contrib.auth.models import User; User.objects.create_superuser('nuts', 's@noova.de', 'tux')" | python manage.py shell

