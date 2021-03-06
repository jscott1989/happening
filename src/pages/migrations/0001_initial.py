# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-02 18:36
from __future__ import unicode_literals

from django.db import migrations, models
import django_pgjson.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_data', django_pgjson.fields.JsonField(default={})),
                ('url', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('content', django_pgjson.fields.JsonField(default={'blockLists': [[], []], 'blocks': []})),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
