# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-19 12:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0055_outputdata_sector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outputdata',
            name='sector_old',
        ),
    ]
