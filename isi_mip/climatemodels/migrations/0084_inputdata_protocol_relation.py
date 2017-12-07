# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-07 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0083_auto_20171116_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputdata',
            name='protocol_relation',
            field=models.CharField(choices=[('P', 'Protocol data'), ('S', 'Supplementary data')], default='P', max_length=1),
        ),
    ]
