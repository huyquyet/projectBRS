from django import forms
from django.forms import TextInput, NumberInput, DateInput

from app.sendbybook.models import ByBook

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class SendNewBookFormView(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = ByBook
        fields = ['name', 'author', 'publish', 'page', 'date']
        widgets = {
            'name': TextInput(attrs={'size': 70, 'required': True}),
            'author': TextInput(attrs={'size': 70, 'required': True}),
            'publish': TextInput(attrs={'size': 70, 'required': True}),
            'page': NumberInput(attrs={'min': '0'}),
            'date': DateInput(attrs={}, format="%Y-%m-%d"),
        }

