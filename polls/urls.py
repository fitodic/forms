# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import CreatePollView, IndexView, InitializeView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^polls/initialize/$', InitializeView.as_view(), name='initialize'),
    url(r'^polls/create/(?P<choices>[0-9]{1})/$', CreatePollView.as_view(),
        name='create'),
]
