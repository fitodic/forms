# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Choice, Question


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):

    list_display = ('choice_text', 'question_text')
    search_fields = ('choice_text',)

    def question_text(self, obj):
        return obj.question.question_text


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = ('question_text', 'choices')
    search_fields = ('question_text',)

    def choices(self, obj):
        return ', '.join(obj.choice_set.values_list('choice_text', flat=True))
