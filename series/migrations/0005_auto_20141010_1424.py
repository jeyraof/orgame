# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0004_episode_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='air_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
