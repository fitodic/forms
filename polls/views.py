# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import FormView

from .forms import InitialForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "polls/index.html"


class InitializeView(LoginRequiredMixin, FormView):
    template_name = 'polls/initialize.html'
    form_class = InitialForm
