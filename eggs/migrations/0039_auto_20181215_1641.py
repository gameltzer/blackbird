# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-15 22:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import eggs.storage


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0038_auto_20181208_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='csvID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eggs.Csv'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sampleFile',
            field=models.FileField(storage=eggs.storage.OverwriteStorage(), upload_to='sample/'),
        ),
    ]