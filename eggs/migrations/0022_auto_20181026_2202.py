# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-27 03:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0021_auto_20181026_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='timeCreated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
