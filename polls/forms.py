# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class InitialForm(forms.Form):
    number_of_choices = forms.IntegerField(
        required=True, min_value=1, max_value=9)
