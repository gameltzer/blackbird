# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 02:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0029_auto_20181206_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='CsvID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eggs.Csv'),
        ),
    ]
