# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)


class Series(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True)
    name = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def episode_count(self):
        return Episode.objects.filter(series=self).count()


class Episode(models.Model):
    series = models.ForeignKey(Series, blank=False)
    episode = models.IntegerField(blank=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    air_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_recordable(self, user):
        return Record.objects.filter(episode=self, user=user).count() < 1

    def record(self, request):
        user = request.user
        r = Record.objects.create(user=user,
                                  series=self.series,
                                  episode=self,
                                  star=0, review='')
        r.save()
        return r
    def save(self, *args, **kwargs):
        self.series.updated_at = timezone.now()
        self.series.save()
        super(Episode,self).save(*args,**kwargs)

class Record(models.Model):
    user = models.ForeignKey(User, blank=False)
    series = models.ForeignKey(Series, blank=False)
    episode = models.ForeignKey(Episode, blank=False)
    star = models.IntegerField(blank=True, null=True)
    review = models.TextField(blank=True)
    view_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series', 'episode', )
