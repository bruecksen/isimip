# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 12:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0041_simulationround_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactmodel',
            name='base_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='impact_model', to='climatemodels.BaseImpactModel'),
        ),
    ]