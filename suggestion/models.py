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
    CANCELED = 3
    STATUS_CHOICE = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELED, 'Canceled'),
    )

    BONUS_KNOWLEDGE = 10

    DELETE = 0
    MODIFY = 1
    WAY_CHOICE = (
        (DELETE, 'Delete'),
        (MODIFY, 'Modify'),
    )

    user = models.ForeignKey(User, blank=False)
    way = models.IntegerField(choices=WAY_CHOICE, default=MODIFY)
    status = models.IntegerField(choices=STATUS_CHOICE, default=PENDING)
    model = models.CharField(max_length=20, choices=SUPPORT_MODEL_CHOICE, blank=False)
    field = models.CharField(max_length=20, blank=True)
    target = models.IntegerField(blank=False, default=0)
    value_type = models.CharField(max_length=20, blank=True)
    value = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, way=MODIFY, user=None, model=None, field=None, target=None, value=u'', comment=u''):
        if not user:
            return None

        if way == cls.DELETE:
            suggest = cls(user=user, way=way,
                          model=model,
                          target=target,
                          comment=comment
                          )
            suggest.save()
            return suggest

        elif way == cls.MODIFY:
            if None in [model, field]:
                return None

            target_model = django_apps.get_model(model)
            if not hasattr(target_model, field):
                return None

            value_type = getattr(target_model, field).get_internal_type()

            suggest = cls(user=user, way=way,
                          model=model, field=field,
                          target=target,
                          value=value, value_type=value_type,
                          comment=comment)
            suggest.save()
            return suggest

        return None

    def approve(self, feedback=u'+1'):
        target_model = django_apps.get_model(self.model)

        try:
            target = target_model.objects.get(id=self.target)
        except target_model.DoesNotExist:
            self.status = self.CANCELED
            self.feedback = u'[Canceled] 대상이 삭제되어 자동 취소 되었습니다.'
            self.save()

            return False

        if self.way == self.DELETE:
            target.delete()

        elif self.way == self.MODIFY:
            value = {
                'DateTimeField': lambda x: strptime(x, '%Y-%m-%d %H:%M:%S'),
                'IntegerField': lambda x: int(x),
                'TextField': lambda x: x,
                'CharField': lambda x: x,
            }.get(self.value_type)(self.value)

            setattr(target, self.field, value)
            target_model.save()

        user_profile = self.user.profile
        user_profile.knowledge += self.BONUS_KNOWLEDGE
        user_profile.save()

        self.status = self.APPROVED
        self.feedback = feedback
        self.save()

        return True

    def reject(self, feedback=u'거절한다!'):
        self.status = self.REJECTED
        self.feedback = feedback
        self.save()
