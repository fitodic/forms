# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import CreateView, FormView

from .forms import InitialForm, QuestionForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "polls/index.html"


class InitializeView(LoginRequiredMixin, FormView):
    template_name = 'polls/initialize.html'
    form_class = InitialForm

    def get_success_url(self):
        form_kwargs = self.get_form_kwargs()
        number_of_choices = form_kwargs.get('number_of_choices', 1)

        url = '/polls/create/{}/'.format(number_of_choices)

        return url


class CreatePollView(LoginRequiredMixin, CreateView):
    template_name = 'polls/create_poll.html'
    form_class = QuestionForm