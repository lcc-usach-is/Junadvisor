from typing import OrderedDict
from django import forms
from django.forms import ModelForm
from .models import *

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ('comercio', 'titulo', 'precio',
         'descripcion', 'menu_pic', 'categoria')