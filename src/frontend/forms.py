# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from datetimewidget.widgets import DateWidget, DateTimeWidget

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory



from bootstrap3.tests import TestForm
from main.utils import TYPE_OF_ORDER

RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
    ('unknown', 'Unknown'),
)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, min_length=6)
    password = forms.CharField(max_length=20, min_length=6, widget=forms.PasswordInput)

class OrderForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'input-lg'
        self.fields['products'].widget.attrs['class'] = 'input-lg'
        self.fields['type_order'].widget.attrs['class'] = 'input-lg'
        self.fields['amount_select'].widget.attrs['class'] = 'input-lg'

    required_css_class = 'bootstrap3-req'

    products = forms.ChoiceField(
        choices=MEDIA_CHOICES,
    )

    type_order = forms.ChoiceField(
        choices=TYPE_OF_ORDER,
    )

    CHOICES_1_to_10 = (
        tuple(range(9, 11)),
        tuple(range(1, 3))
    )

    CHOICES = []
    for x in  range(1, 11):
        CHOICES.append((str(x), str(x),))

    for x in  range(15, 55, 5):
        CHOICES.append((str(x), str(x),))

    amount_select = forms.ChoiceField(
        choices=(
            ('Amount', (
                CHOICES)
            ),
        ),
        help_text='Check as many as you like.',
    )

    date = forms.DateField(
        input_formats=['%Y-%m-%d', '%d-%m-%Y'],
        initial=datetime.now().date(),
        widget=DateTimePicker(options={"format": "DD-MM-YYYY",
                                       "pickTime": False}))


class ContactForm(TestForm):
    pass


class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        #raise forms.ValidationError("This error was added to show the non form errors styling")

ContactFormSet = formset_factory(TestForm, formset=ContactBaseFormSet,
                                 extra=2,
                                 max_num=4,
                                 validate_max=True)

OrderFormSet = formset_factory(OrderForm, formset=ContactBaseFormSet,
                                 extra=1,
                                 max_num=4,
                                 validate_max=True)


class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data