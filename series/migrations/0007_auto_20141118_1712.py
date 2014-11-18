# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0006_auto_20141013_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='updated_at',
            field=models.DateTimeField(default=datetime.date(2014, 11, 18), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='star',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
