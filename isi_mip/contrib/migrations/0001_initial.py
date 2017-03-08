# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-07 09:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('climatemodels', '0077_auto_20170301_1209'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.CharField(blank=True, max_length=500, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('role', models.ManyToManyField(blank=True, related_name='user_roles', to='contrib.Role')),
                ('sector', models.ManyToManyField(blank=True, related_name='user_sectors', to='climatemodels.Sector')),
                ('simulation_round', models.ManyToManyField(blank=True, related_name='user_simulationrounds', to='climatemodels.SimulationRound')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
