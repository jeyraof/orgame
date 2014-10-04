# -*- coding: utf-8 -*-
from django.db import models
from series.models import Series, Episode


class User(models.Model):
    MEMBER = 0
    MODERATOR = 1
    ADMIN = 2
    ROLE_CHOICES = (
        (MEMBER, 'Member'),
        (MODERATOR, 'Blocked User'),
        (ADMIN, 'Admin'),
    )

    nickname = models.CharField(max_length=50, blank=True, unique=True, null=True)
    email = models.CharField(max_length=100, blank=True, unique=True, null=True)
    role = models.IntegerField(choices=ROLE_CHOICES, blank=False, default=0)
    knowledge = models.IntegerField(blank=False, default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def new(cls):
        new_user = cls(email=None, nickname=None)
        new_user.save()
        return new_user

    @classmethod
    def get_by(cls, member_id):
        if not member_id:
            return None

        user = list(cls.objects.filter(id=member_id))
        if user:
            return user[0]
        return None

    def merge_with(self, other_user):
        # 새로운 Social 타입이 생길때를 대비해서 작성할 예정
        # FB_user.merge_with(other_social_user) -> 두 유져 병합
        # knowledge 처리가 곤란하다. 한쪽을 버리게 하던지, 재계산이 필요할듯.
        pass

    def sign_in(self, request):
        request.session['member_id'] = self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_staff(self):
        return self.role > self.MEMBER

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class SocialOAuth(models.Model):
    FACEBOOK = 1
    PROVIDER_CHOICES = (
        (FACEBOOK, 'Facebook'),
    )

    user = models.ForeignKey(User, blank=False)
    provider = models.IntegerField(choices=PROVIDER_CHOICES, blank=False)
    uid = models.CharField(max_length=100)

    @classmethod
    def join(cls, provider, uid):
        new_user = User.new()
        new_oauth = cls(user=new_user, provider=provider, uid=uid)
        new_oauth.save()
        return new_oauth

    def login(self):
        self.user.login()


class Record(models.Model):
    user = models.ForeignKey(User, blank=False)
    series = models.ForeignKey(Series, blank=False)
    episode = models.ForeignKey(Episode, blank=False)
    star = models.IntegerField(blank=True)
    review = models.TextField(blank=True)
    view_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series', 'episode', )
