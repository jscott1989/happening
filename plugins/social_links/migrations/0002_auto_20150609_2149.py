# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_links', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]