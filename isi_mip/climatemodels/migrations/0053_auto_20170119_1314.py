# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-19 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def set_sectors(apps, schema_editor):
    SectorModel = apps.get_model('climatemodels', 'Sector')
    BaseImpactModel = apps.get_model('climatemodels', 'BaseImpactModel')
    for bim in BaseImpactModel.objects.all():
        bim.sector = SectorModel.objects.get(name=bim.sector_old)
        bim.save()


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0052_auto_20170119_1313'),
    ]

    operations = [

        migrations.AlterModelOptions(
            name='baseimpactmodel',
            options={'ordering': ('name', 'sector')},
        ),
        migrations.AddField(
            model_name='baseimpactmodel',
            name='sector',
            field=models.ForeignKey(default=1, help_text='The sector to which this information pertains. Some models may have further entries for other sectors.', on_delete=django.db.models.deletion.CASCADE, to='climatemodels.Sector'),
            preserve_default=False,
        ),
        migrations.RunPython(
            set_sectors
        ),
    ]
