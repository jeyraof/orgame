# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)


class Series(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True)
    name = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def episode_count(self):
        return Episode.objects.filter(series=self).count()


class Episode(models.Model):
    series = models.ForeignKey(Series, blank=False)
    episode = models.IntegerField(blank=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    air_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Record(models.Model):
    user = models.ForeignKey(User, blank=False)
    series = models.ForeignKey(Series, blank=False)
    episode = models.ForeignKey(Episode, blank=False)
    star = models.IntegerField(blank=True)
    review = models.TextField(blank=True)
    view_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series', 'episode', )
