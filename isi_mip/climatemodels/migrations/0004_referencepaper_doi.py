# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0003_auto_20160228_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencepaper',
            name='doi',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
