# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0009_vcfrow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vcfrow',
            name='result',
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='alt',
            field=models.CharField(default='.', max_length=100),
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='chrom',
            field=models.CharField(default='.', max_length=100),
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='filterColInFile',
            field=models.CharField(default='.', max_length=100),
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='formatColInFile',
            field=models.CharField(default='.', max_length=5000),
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='idColInFile',
            field=models.CharField(default='.', max_length=100),
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='info',
            field=models.CharField(default='.', max_length=5000),
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='qual',
            field=models.CharField(default='.', max_length=100),
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='ref',
            field=models.CharField(default='.', max_length=100),
        ),
    ]