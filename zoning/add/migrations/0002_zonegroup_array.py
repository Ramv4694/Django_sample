# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-22 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zonegroup',
            name='Array',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
