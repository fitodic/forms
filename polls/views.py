# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import (CreateView,
                                  FormView,
                                  ListView,
                                  UpdateView)

from .forms import InitialForm, QuestionForm, ChoiceForm
from .models import Choice, Question


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "polls/index.html"


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "polls/list_polls.html"
    context_object_name = 'questions'


class VoteView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = "polls/poll_vote.html"
    context_object_name = 'question'
    fields = ['question_text']

    def post(self, request, *args, **kwargs):
        choice_id = request.POST.get('choice', None)
        if choice_id:
            try:
                choice = Choice.objects.get(id=choice_id)
            except Choice.DoesNotExist:
                return self.form_invalid()
            question_id = kwargs.get('pk', None)
            if question_id and choice.question_id == int(question_id):
                return self.form_valid(choice=choice)
        else:
            return self.form_invalid()

    def form_valid(self, choice):
        choice.voters.add(self.request.user)
        choice.save()

        return render(
            self.request,
            self.template_name,
            {
                'question': choice.question,
                'chosen_answer': choice
            })

    def form_invalid(self):
        question_id = self.kwargs.get('pk')
        question = Question.objects.get(pk=question_id)

        return render(
            self.request,
            self.template_name,
            {
                'question': question,
                'error_message': 'Please select an answer.'
            })


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
    success_url = '/polls/'

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
