# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=50, unique=True, null=True, blank=True)),
                ('email', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('role', models.IntegerField(default=0, choices=[(0, b'Member'), (1, b'Moderator'), (2, b'Admin')])),
                ('knowledge', models.IntegerField(default=0)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('star', models.IntegerField(blank=True)),
                ('review', models.TextField(blank=True)),
                ('view_at', models.DateTimeField(auto_now_add=True)),
                ('episode', models.ForeignKey(to='series.Episode')),
                ('series', models.ForeignKey(to='series.Series')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('uid', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('user', 'series', 'episode')]),
        ),
    ]
