# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
                    CreatePollView,
                    IndexView,
                    InitializeView,
                    QuestionDetailView,
                    QuestionListView)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^polls/$', QuestionListView.as_view(), name='polls'),
    url(r'^polls/(?P<pk>[0-9]+)/$', QuestionDetailView.as_view(),
        name='detail'),
    url(r'^polls/initialize/$', InitializeView.as_view(), name='initialize'),
    url(r'^polls/create/(?P<choices>[1-9]{1})/$', CreatePollView.as_view(),
        name='create'),
]
