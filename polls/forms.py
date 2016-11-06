# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Choice, Question


class InitialForm(forms.Form):
    number_of_choices = forms.IntegerField(
        required=True, min_value=1, max_value=9)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)

