# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-17 23:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0002_auto_20181009_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('batchName', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('timeCreated', models.TimeField(auto_now_add=True)),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='eggs.Reference')),
            ],
        ),
        migrations.RemoveField(
            model_name='sample',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='reference',
        ),
    ]