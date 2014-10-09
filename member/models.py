# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from hashlib import md5
from orgame.settings import SECRET_KEY


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
