# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-18 09:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0013_auto_20160418_0835'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output', models.TextField(blank=True, help_text='Is output (e.g. PFT cover) written out per grid-cell area or per land and water area within a grid cell, or land only?', null=True, verbose_name='Output format')),
                ('output_per_pft', models.TextField(blank=True, help_text='Is output per PFT per unit area of that PFT, i.e. requiring weighting by the fractional coverage of each PFT to get the gridbox average?', null=True)),
                ('considerations', models.TextField(blank=True, help_text='Things to consider, when calculating basic variables such as GPP, NPP, RA, RH from the model.', null=True)),
                ('dynamic_vegetation', models.TextField(blank=True, null=True)),
                ('nitrogen_limitation', models.TextField(blank=True, null=True)),
                ('co2_effects', models.TextField(blank=True, null=True)),
                ('light_interception', models.TextField(blank=True, null=True)),
                ('light_utilization', models.TextField(blank=True, help_text='photosynthesis, RUE- approach?', null=True)),
                ('phenology', models.TextField(blank=True, null=True)),
                ('water_stress', models.TextField(blank=True, null=True)),
                ('heat_stress', models.TextField(blank=True, null=True)),
                ('evapotranspiration_approach', models.TextField(blank=True, null=True, verbose_name='Evapo-transpiration approach')),
                ('rooting_depth_differences', models.TextField(blank=True, help_text='Include how it changes.', null=True, verbose_name='Differences in rooting depth')),
                ('root_distribution', models.TextField(blank=True, null=True, verbose_name='Root distribution over depth')),
                ('permafrost', models.TextField(blank=True, null=True)),
                ('closed_energy_balance', models.TextField(blank=True, null=True)),
                ('soil_moisture_surface_temperature_coupling', models.TextField(blank=True, null=True, verbose_name='Coupling/feedback between soil moisture and surface temperature')),
                ('latent_heat', models.TextField(blank=True, null=True)),
                ('sensible_heat', models.TextField(blank=True, null=True)),
                ('mortality_age', models.TextField(blank=True, null=True, verbose_name='Age')),
                ('mortality_fire', models.TextField(blank=True, null=True, verbose_name='Fire')),
                ('mortality_drought', models.TextField(blank=True, null=True, verbose_name='Drought')),
                ('mortality_insects', models.TextField(blank=True, null=True, verbose_name='Insects')),
                ('mortality_storm', models.TextField(blank=True, null=True, verbose_name='Storm')),
                ('mortality_stochastic_random_disturbance', models.TextField(blank=True, null=True, verbose_name='Stochastic random disturbance')),
                ('mortality_other', models.TextField(blank=True, null=True, verbose_name='Other')),
                ('mortality_remarks', models.TextField(blank=True, null=True, verbose_name='Remarks')),
                ('nbp_fire', models.TextField(blank=True, null=True, verbose_name='Fire')),
                ('nbp_landuse_change', models.TextField(blank=True, help_text='Deforestation, harvest and other land-use changes', null=True, verbose_name='Land-use change')),
                ('nbp_harvest', models.TextField(blank=True, help_text='1: crops, 2: harvest from forest management, 3: harvest from grassland management', null=True, verbose_name='Harvest')),
                ('nbp_other', models.TextField(blank=True, null=True, verbose_name='Other processes')),
                ('nbp_comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('list_of_pfts', models.TextField(blank=True, help_text='Provide a list of PFTs using the folllowing format: <pft1_long_name> (<pft1_short_name>); <pft2_long_name> (<pft2_short_name>). Include long name in brackets if no short name is available.', null=True, verbose_name='List of PFTs')),
                ('pfts_comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('impact_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='climatemodels.ImpactModel')),
            ],
            options={
                'verbose_name_plural': 'Forests',
                'verbose_name': 'Forests',
            },
        ),
        migrations.AlterModelOptions(
            name='biomes',
            options={'verbose_name': 'Biomes', 'verbose_name_plural': 'Biomes'},
        ),
        migrations.AlterModelOptions(
            name='marineecosystemsglobal',
            options={'verbose_name': 'Marine Ecosystems and Fisheries (global)', 'verbose_name_plural': 'Marine Ecosystems and Fisheries (global)'},
        ),
        migrations.AlterModelOptions(
            name='marineecosystemsregional',
            options={'verbose_name': 'Marine Ecosystems and Fisheries (regional)', 'verbose_name_plural': 'Marine Ecosystems and Fisheries (regional)'},
        ),
        migrations.AlterModelOptions(
            name='waterglobal',
            options={'verbose_name': 'Water (global)', 'verbose_name_plural': 'Water (global)'},
        ),
        migrations.AlterModelOptions(
            name='waterregional',
            options={'verbose_name': 'Water (regional)', 'verbose_name_plural': 'Water (regional)'},
        ),
    ]
