# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-19 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0059_auto_20170119_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sectorinformationfield',
            options={'ordering': ('order', 'name'), 'verbose_name_plural': 'Sector information fields'},
        ),
        migrations.AlterModelOptions(
            name='sectorinformationgroup',
            options={'ordering': ('order', 'name'), 'verbose_name_plural': 'Sector information groups'},
        ),
        migrations.AddField(
            model_name='sectorinformationfield',
            name='order',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sectorinformationgroup',
            name='order',
            field=models.SmallIntegerField(default=0),
        ),
    ]
