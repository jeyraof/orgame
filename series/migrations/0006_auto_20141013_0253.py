# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0005_auto_20141010_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='extra_info',
        ),
        migrations.RemoveField(
            model_name='series',
            name='extra_info',
        ),
        migrations.AddField(
            model_name='episode',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2014, 10, 13), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2014, 10, 13), auto_now_add=True),
            preserve_default=False,
        ),
    ]
