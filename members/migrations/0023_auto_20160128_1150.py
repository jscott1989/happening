# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import happening.storage


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0022_auto_20160127_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promocode',
            name='activate_tag_on_use',
        ),
        migrations.RemoveField(
            model_name='promocodeuse',
            name='promocode',
        ),
        migrations.RemoveField(
            model_name='promocodeuse',
            name='user',
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to=happening.storage.inner),
        ),
        migrations.DeleteModel(
            name='Promocode',
        ),
        migrations.DeleteModel(
            name='PromocodeUse',
        ),
    ]
