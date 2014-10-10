# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0002_auto_20141009_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='category',
            field=models.ForeignKey(blank=True, to='series.Category', null=True),
        ),
    ]
