# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0010_auto_20181019_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vcfrow',
            name='id',
        ),
        migrations.AddField(
            model_name='vcfrow',
            name='rowid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]