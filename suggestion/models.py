# -*- coding: utf-8 -*-
from django.apps import apps as django_apps
from django.db import models
from django.contrib.auth.models import User
from time import strptime


class Suggestion(models.Model):
    SERIES = 'series.Series'
    EPISODE = 'series.Episode'
    SUPPORT_MODEL_CHOICE = (
        (SERIES, 'Series'),
        (EPISODE, 'Episode'),
    )

    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    STATUS_CHOICE = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )

    BONUS_KNOWLEDGE = 10

    user = models.ForeignKey(User, blank=False)
    status = models.IntegerField(choices=STATUS_CHOICE, default=PENDING)
    model = models.CharField(max_length=20, choices=SUPPORT_MODEL_CHOICE, blank=False)
    field = models.CharField(max_length=20, blank=False)
    value_type = models.CharField(max_length=20, blank=False)
    value = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, user=None, model=None, field=None, value=u'', comment=u''):
        if None in [user, model, field]:
            return None

        target_model = django_apps.get_model(model)
        if not hasattr(target_model, field):
            return None
        value_type = getattr(target_model, field).get_internal_type()

        suggest = cls(user=user, model=model, field=field,
                      value=value, value_type=value_type,
                      comment=comment)
        suggest.save()
        return suggest

    def approve(self, feedback=u'+1'):
        value = {
            'DateTimeField': lambda x: strptime(x, '%Y-%m-%d %H:%M:%S'),
            'IntegerField': lambda x: int(x),
            'TextField': lambda x: x,
            'CharField': lambda x: x,
        }.get(self.value_type)(self.value)

        target_model = django_apps.get_model(self.model)
        setattr(target_model, self.field, value)
        target_model.save()

        user_profile = self.user.profile
        user_profile.knowledge += self.BONUS_KNOWLEDGE
        user_profile.save()

        self.status = self.APPROVED
        self.feedback = feedback
        self.save()

    def reject(self, feedback=u'거절한다!'):
        self.status = self.REJECTED
        self.feedback = feedback
        self.save()
