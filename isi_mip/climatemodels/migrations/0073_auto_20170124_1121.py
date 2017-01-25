# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 10:21
from __future__ import unicode_literals

from django.db import migrations, models


def set_data_sets(apps, schema_editor):
    InputDataInformation = apps.get_model('climatemodels', 'InputDataInformation')
    for idi in InputDataInformation.objects.all():
        sr = idi.impact_model.simulation_round
        idi.emissions_data_sets = idi.climate_data_sets.filter(data_type__name='Emissions', simulation_round=sr)
        idi.land_use_data_sets = idi.climate_data_sets.filter(data_type__name='Land use', simulation_round=sr)
        idi.observed_atmospheric_climate_data_sets = idi.climate_data_sets.filter(data_type__name='Observed atmospheric climate', simulation_round=sr)
        idi.observed_ocean_climate_data_sets = idi.climate_data_sets.filter(data_type__name='Observed ocean climate', simulation_round=sr)
        idi.other_data_sets = idi.climate_data_sets.filter(data_type__name='Other', simulation_round=sr)
        idi.other_human_influences_data_sets = idi.climate_data_sets.filter(data_type__name='Other human influences', simulation_round=sr)
        idi.simulated_atmospheric_climate_data_sets = idi.climate_data_sets.filter(data_type__name='Simulated atmospheric climate', simulation_round=sr)
        idi.simulated_ocean_climate_data_sets = idi.climate_data_sets.filter(data_type__name='Simulated ocean climate', simulation_round=sr)
        idi.socio_economic_data_sets = idi.climate_data_sets.filter(data_type__name='Socio-economic', simulation_round=sr)
        idi.save()


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0072_auto_20170123_1059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inputdata',
            options={'ordering': ('-created', 'name'), 'verbose_name_plural': 'Input data'},
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='emissions_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The emissions data sets used in this simulation round', related_name='emissions_data_sets', to='climatemodels.InputData', verbose_name='Emissions data sets used'),
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='land_use_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The Land use data sets used in this simulation round', related_name='land_use_data_sets', to='climatemodels.InputData', verbose_name='Land use data sets used'),
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='observed_atmospheric_climate_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The observed atmospheric climate data sets used in this simulation round', related_name='observed_atmospheric_climate_data_sets', to='climatemodels.InputData', verbose_name='Observed atmospheric climate data sets used'),
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='observed_ocean_climate_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The observed ocean climate data sets used in this simulation round', related_name='observed_ocean_climate_data_sets', to='climatemodels.InputData', verbose_name='Observed ocean climate data sets used'),
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='other_data_sets',
            field=models.ManyToManyField(blank=True, help_text='Other data sets used in this simulation round', related_name='other_data_sets', to='climatemodels.InputData', verbose_name='Other data sets used'),
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='other_human_influences_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The other human influences data sets used in this simulation round', related_name='other_human_influences_data_sets', to='climatemodels.InputData', verbose_name='Other human influences data sets used'),
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='simulated_atmospheric_climate_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The simulated atmospheric climate data sets used in this simulation round', related_name='simulated_atmospheric_climate_data_sets', to='climatemodels.InputData', verbose_name='Simulated atmospheric climate data sets used'),
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='simulated_ocean_climate_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The observed ocean climate data sets used in this simulation round', related_name='simulated_ocean_climate_data_sets', to='climatemodels.InputData', verbose_name='Simulated ocean climate data sets used'),
        ),
        migrations.AddField(
            model_name='inputdatainformation',
            name='socio_economic_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The socio-economic data sets used in this simulation round', related_name='socio_economic_data_sets', to='climatemodels.InputData', verbose_name='Socio-economic data sets used'),
        ),
        migrations.AlterField(
            model_name='inputdatainformation',
            name='climate_data_sets',
            field=models.ManyToManyField(blank=True, help_text='The climate-input data sets used in this simulation round', related_name='climate_data_sets', to='climatemodels.InputData', verbose_name='Climate data sets used'),
        ),
        migrations.RunPython(
            set_data_sets
        ),
    ]