# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-23 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add', '0003_auto_20181022_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arraygroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Location', models.CharField(max_length=30)),
                ('Class', models.CharField(max_length=30)),
                ('Array', models.CharField(max_length=100)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='zonegroup',
            options={'managed': True},
        ),
    ]
