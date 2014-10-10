# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suggestion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='target',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='suggestion',
            name='way',
            field=models.IntegerField(default=1, choices=[(0, b'Delete'), (1, b'Modify')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='field',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Pending'), (1, b'Approved'), (2, b'Rejected'), (3, b'Canceled')]),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='value_type',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
