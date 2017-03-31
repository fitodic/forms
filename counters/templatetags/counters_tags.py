# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django import template
from ..utils import get_key_value, redis_is_active

register = template.Library()


@register.simple_tag(takes_context=True)
def get_page_count(context):
    if redis_is_active():
        return get_key_value(context.request.path)
