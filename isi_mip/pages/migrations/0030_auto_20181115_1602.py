# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-15 15:02
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0029_auto_20181114_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperpagetag',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='paperpage',
            name='tags',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='paper_page', to='pages.PaperPageTag'),
        ),
    ]
