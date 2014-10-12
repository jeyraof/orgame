# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def highlight(html, keyword):
    html = html.replace(keyword, '<em>' + keyword + '</em>')
    return html