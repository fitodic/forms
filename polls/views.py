# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.views.generic import TemplateView
from django.views.generic import CreateView, FormView

from .forms import InitialForm, QuestionForm, ChoiceForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "polls/index.html"


class InitializeView(LoginRequiredMixin, FormView):
    template_name = 'polls/initialize.html'
    form_class = InitialForm

    def get_success_url(self):
        form_kwargs = self.get_form_kwargs()
        form_data = form_kwargs.get('data')
        number_of_choices = form_data.get('number_of_choices', 1)
        url = '/polls/create/{}/'.format(number_of_choices)

        return url


class CreatePollView(LoginRequiredMixin, CreateView):
    template_name = 'polls/create_poll.html'
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.object = None
        question_form = self.get_form()

        choices = kwargs.get('choices', 1)
        choice_form = formset_factory(ChoiceForm, extra=int(choices))

        return self.render_to_response(
            self.get_context_data(
                question_form=question_form, choice_form=choice_form))
