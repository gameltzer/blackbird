# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-18 22:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eggs', '0008_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='VCFRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eggs.Result')),
            ],
        ),
    ]