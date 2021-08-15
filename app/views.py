from typing import ContextManager

from django.contrib import auth

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import *
from .models import *
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='estudiante')
            user.groups.add(group)
            Estudiante.objects.create(user=user, username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email)
            
            messages.success(request, 'Cuenta creada para ' + username)
            
            return redirect('login')
        else:
            password1 = form.data['password1']
            password2 = form.data['password2']
            for msg in form.errors.as_data():
                if msg == 'email':
                    messages.error(request, "El email no es valido")
                if msg == 'password2' and password1 == password2:
                    messages.error(request, "La contraseña no es segura")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request, "Las contraseñas no coinciden")          

    context= {'form': form}
    return render(request, 'app/register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credenciales Invalidas')

    context= {}
    return render(request, 'app/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

##### PAGES #####
def home(request):
    menus = Menu.objects.filter(is_active = True)
    context = {'menus': menus}

    return render(request, 'app/dashboard.html', context)

def ingresarMenu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MenuForm()

    context = {'form': form}
    return render(request, 'app/menu_form.html', context)

def vistaMenu(request, pk):

    form = ComentarioForm()
    menu = Menu.objects.get(id=pk)
    comentarios = menu.comentario_set.filter(is_active = True)
    
    if request.user.is_authenticated and not request.user.is_staff:
        estudiante = Estudiante.objects.get(user=request.user)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.instance.estudiante = estudiante
            form.instance.menu = menu
            form.save()
            return redirect('/menu/' + pk)

    context = { 'menu': menu, 'comentarios': comentarios, 'form': form}

    return render(request, "app/menu.html", context)