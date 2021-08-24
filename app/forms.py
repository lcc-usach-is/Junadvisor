from typing import OrderedDict
from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class EstudianteForm(ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'
        exclude = ['user']

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ('comercio', 'titulo', 'precio',
         'descripcion', 'menu_pic', 'categoria', 'is_active')

class IngresarMenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ('comercio', 'titulo', 'precio',
         'descripcion', 'menu_pic', 'categoria')

class ComercioForm(ModelForm):
    class Meta:
        model = Comercio
        fields = ('nombre', 'descripcion', 'direccion', 'is_active')
    
    

class IngresarComercioForm(ModelForm):
    class Meta:
        model = Comercio
        fields = ('nombre', 'descripcion', 'direccion') 

class ComentarioForm(forms.Form):
    CHOICES=[(1, '1: Muy malo'),(2, '2: Malo'), (3, '3: Decente'), (4, '4: Bueno'), (5, '5: Excelente')]

    contenido = forms.CharField(widget=forms.Textarea)
    calificacion = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
    def __init__(self, *args, **kwargs):
        super(ComentarioForm, self).__init__(*args, **kwargs)
        self.fields['contenido'].widget.attrs['rows'] = 3

class EstudianteForm(ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'
        exclude = ['user']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class IngresarRecomendacionForm(ModelForm):
    contenido = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Recomendacion
        fields = ('nombre',)
    
    def __init__(self, *args, **kwargs):
        super(IngresarRecomendacionForm, self).__init__(*args, **kwargs)
        self.fields['contenido'].widget.attrs['rows'] = 3
    
    