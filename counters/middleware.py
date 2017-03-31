# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .utils import redis_is_active, increment_by, get_key_value


class CounterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        super(CounterMiddleware, self).__init__()

    def __call__(self, request):

        if redis_is_active():
            increment_by(request.path)

        response = self.get_response(request)
        return response
