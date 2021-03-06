# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-07 22:28
from __future__ import unicode_literals

import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Microsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=63)),
                ('subdomain', models.CharField(db_index=True, max_length=127)),
                ('values', jsonfield.fields.JSONField(blank=True)),
            ],
            options={
                'db_table': 'ednx_microsites_microsite',
            },
        ),
    ]
