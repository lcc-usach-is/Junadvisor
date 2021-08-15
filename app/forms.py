from typing import OrderedDict
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ('comercio', 'titulo', 'precio',
         'descripcion', 'menu_pic', 'categoria')

class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ('contenido', 'calificacion')

class EstudianteForm(ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'
        exclude = ['user']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']