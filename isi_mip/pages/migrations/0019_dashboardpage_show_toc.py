# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-08 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_auto_20170301_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardpage',
            name='show_toc',
            field=models.BooleanField(default=False, help_text='Show Table of Contents'),
        ),
    ]
