# -*- coding: utf-8 -*-
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)


class Series(models.Model):
    category = models.ForeignKey(Category, blank=True)
    name = models.CharField(max_length=255)
    extra_info = models.TextField(blank=True)


class Episode(models.Model):
    series = models.ForeignKey(Series, blank=False)
    episode = models.IntegerField(blank=False)
    air_at = models.DateTimeField(blank=True)
    extra_info = models.TextField(blank=True)