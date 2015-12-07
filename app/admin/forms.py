from django import forms
from django.forms import TextInput, Textarea, NumberInput, DateInput

from app.book.models import Book
from app.category.models import Category

__author__ = 'FRAMGIA\nguyen.huy.quyet'


class BookCreateFormView(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Book
        fields = ['title', 'slug', 'category', 'description', 'author', 'publish', 'page', 'price', 'date', 'cover']
        widgets = {
            'title': TextInput(attrs={'size': 70, 'required': True}),
            'slug': TextInput(attrs={'size': 70, 'required': True}),
            'description': Textarea(attrs={'rows': 7, 'cols': 70}),
            'author': TextInput(attrs={'size': 70, 'required': True}),
            'publish': TextInput(attrs={'size': 70, 'required': True}),
            'page': NumberInput(attrs={'min': '0'}),
            'price': NumberInput(attrs={'min': '0'}),
            'date': DateInput(attrs={}, format="%Y-%m-%d"),

        }
