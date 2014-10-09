# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from hashlib import md5
from orgame.settings import SECRET_KEY
import re


class Profile(models.Model):
    user = models.OneToOneField(User)

    MEMBER = 0
    MODERATOR = 1
    ADMIN = 2
    ROLE_CHOICES = (
        (MEMBER, 'Member'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    nickname = models.CharField(max_length=50, blank=True, unique=True, null=True)
    email = models.CharField(max_length=100, blank=True, unique=True, null=True)
    role = models.IntegerField(choices=ROLE_CHOICES, blank=False, default=0)
    knowledge = models.IntegerField(blank=False, default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_staff(self):
        return self.role > self.MEMBER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_newbie(self):
        if not self.nickname or not self.email:
            return True
        return False

    @classmethod
    def validate_nickname(cls, nickname=None):
        if re.match("^[A-Za-z0-9_-]*$", nickname or ''):
            try:
                cls.objects.get(nickname=nickname)
                return False, '이미 존재하는 닉네임 입니다.'

            except cls.DoesNotExist:
                return True, None

        return False, '알파벳, 숫자, _, - 만 사용 가능합니다.'

    @classmethod
    def validate_email(cls, email=None):
        if re.match("[^@]+@[^@]+\.[^@]+", email or ''):
            try:
                cls.objects.get(email=email)
                return False, '이미 존재하는 이메일 입니다.'

            except cls.DoesNotExist:
                return True, None

        return False, '올바른 이메일을 입력해주세요.'


class SocialOAuth(models.Model):
    FACEBOOK = 1
    PROVIDER_CHOICES = (
        (FACEBOOK, 'Facebook'),
    )

    user = models.ForeignKey(User, blank=False)
    provider = models.IntegerField(choices=PROVIDER_CHOICES, blank=False)
    uid = models.CharField(max_length=100)

    @classmethod
    def join(cls, provider, uid, profile=None):
        if not profile:
            return None

        user_info = {
            'username': profile.get('name', ''),
            'email': '{account}@facebook.com'.format(account=profile.get('id', '')),
            'password': md5(profile.get('name', '') + SECRET_KEY).hexdigest(),
        }
        new_user = User.objects.create_user(**user_info)
        new_user.save()

        user_profile = Profile(user=new_user)
        user_profile.save()

        new_oauth = cls(user=new_user, provider=provider, uid=uid)
        new_oauth.save()
        return new_oauth
