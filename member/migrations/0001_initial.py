# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('star', models.IntegerField(blank=True)),
                ('review', models.TextField(blank=True)),
                ('view_at', models.DateTimeField(auto_now_add=True)),
                ('episode', models.ForeignKey(to='series.Episode')),
                ('series', models.ForeignKey(to='series.Series')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialOAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.IntegerField(choices=[(1, b'Facebook')])),
                ('uid', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=50, unique=True, null=True, blank=True)),
                ('role', models.IntegerField(default=0, choices=[(0, b'Member'), (1, b'Blocked User'), (2, b'Admin')])),
                ('knowledge', models.IntegerField(default=0)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='socialoauth',
            name='user',
            field=models.ForeignKey(to='member.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='user',
            field=models.ForeignKey(to='member.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('user', 'series', 'episode')]),
        ),
    ]
