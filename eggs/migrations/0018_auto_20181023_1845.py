# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-23 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0017_auto_20181023_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='vcfrow',
            name='formatNameColInFile',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='formatValueColInFile',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
