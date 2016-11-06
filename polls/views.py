# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import CreateView, FormView

from .forms import InitialForm, QuestionForm, ChoiceForm
from .models import Choice, Question


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

    def post(self, request, *args, **kwargs):
        self.object = None
        data = self.request.POST

        question_form = self.get_form()
        ChoiceFormSet = formset_factory(ChoiceForm)
        choice_form = ChoiceFormSet(data)

        if question_form.is_valid() and choice_form.is_valid():
            return self.form_valid(
                question_form=question_form, choice_form=choice_form)
        else:
            return self.form_invalid(
                question_form=question_form, choice_form=choice_form)

    def form_valid(self, question_form, choice_form):
        self.object = Question(
            author=self.request.user,
            question_text=question_form.cleaned_data.get('question_text'))
        self.object.save()

        choices = [
            Choice(question=self.object,
                   choice_text=choice.get('choice_text'))
            for choice in choice_form.cleaned_data
        ]
        Choice.objects.bulk_create(choices)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, question_form, choice_form):
        return self.render_to_response(
            self.get_context_data(
                question_form=question_form, choice_form=choice_form))
