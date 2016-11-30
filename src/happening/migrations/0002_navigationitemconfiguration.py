# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happening', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavigationItemConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'abstract': False,
                'ordering': ('order',),
            },
        ),
    ]
