# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-19 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0014_auto_20160418_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgroEconomicModelling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impact_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='climatemodels.ImpactModel')),
            ],
            options={
                'verbose_name_plural': 'Agro-Economic Modelling',
                'verbose_name': 'Agro-Economic Modelling',
            },
        ),
        migrations.CreateModel(
            name='ComputableGeneralEquilibriumModelling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impact_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='climatemodels.ImpactModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='inputdata',
            old_name='data_set',
            new_name='name',
        ),
        migrations.AddField(
            model_name='inputdata',
            name='caveats',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inputdata',
            name='scenario',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='inputdata',
            name='variables',
            field=models.ManyToManyField(blank=True, to='climatemodels.ClimateVariable'),
        ),
    ]