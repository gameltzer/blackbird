# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-20 03:40
from __future__ import unicode_literals

from django.db import migrations, models
import eggs.storage


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0025_auto_20181028_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='referenceFile',
            field=models.FileField(storage=eggs.storage.OverwriteStorage(), upload_to='reference/'),
        ),
    ]