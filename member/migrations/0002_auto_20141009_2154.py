# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='record',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='record',
            name='series',
        ),
        migrations.RemoveField(
            model_name='record',
            name='user',
        ),
        migrations.DeleteModel(
            name='Record',
        ),
    ]
