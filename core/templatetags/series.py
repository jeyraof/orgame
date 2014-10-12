# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def is_recordable(episode, user):
    return episode.is_recordable(user)
