from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class UserIndex(TemplateView):
    pass

UserIndexView = UserIndex.as_view()