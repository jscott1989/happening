# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-23 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]