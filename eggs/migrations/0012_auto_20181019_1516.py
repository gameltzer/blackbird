# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 20:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0011_auto_20181019_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vcfrow',
            name='alt',
        ),
        migrations.RemoveField(
            model_name='vcfrow',
            name='chrom',
        ),
        migrations.RemoveField(
            model_name='vcfrow',
            name='filterColInFile',
        ),
        migrations.RemoveField(
            model_name='vcfrow',
            name='formatColInFile',
        ),
        migrations.RemoveField(
            model_name='vcfrow',
            name='idColInFile',
        ),
        migrations.RemoveField(
            model_name='vcfrow',
            name='info',
        ),
        migrations.RemoveField(
            model_name='vcfrow',
            name='qual',
        ),
        migrations.RemoveField(
            model_name='vcfrow',
            name='ref',
        ),
    ]