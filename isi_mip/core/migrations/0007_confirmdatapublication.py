# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-15 10:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('core', '0006_auto_20170306_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmDataPublication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='[ISIMIP] Registration invitation for impact-model database', help_text='Invitation subject', max_length=500)),
                ('body', models.TextField(help_text='You can use the following tokens in the email template: {{model_contact_person}}, {{simulation_round}}, {{sector}}. {{impact_model}}')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
