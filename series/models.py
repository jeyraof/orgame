# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)


class Series(models.Model):
    category = models.ForeignKey(Category, blank=True)
    name = models.CharField(max_length=255, db_index=True)
    extra_info = models.TextField(blank=True)


class Episode(models.Model):
    series = models.ForeignKey(Series, blank=False)
    episode = models.IntegerField(blank=False)
    air_at = models.DateTimeField(blank=True)
    extra_info = models.TextField(blank=True)


class Record(models.Model):
    user = models.ForeignKey(User, blank=False)
    series = models.ForeignKey(Series, blank=False)
    episode = models.ForeignKey(Episode, blank=False)
    star = models.IntegerField(blank=True)
    review = models.TextField(blank=True)
    view_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series', 'episode', )
