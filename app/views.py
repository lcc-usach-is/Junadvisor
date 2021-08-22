from typing import ContextManager

from django.contrib import auth

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Avg

from .forms import *
from .models import *
from .filters import *
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
    menus = Menu.objects.filter(comercio__is_active = True, is_active = True)

    context = {'menus': menus}

    return render(request, 'app/dashboard.html', context)

### ADMIN MENU ###
def administrarMenu(request):
    menus = Menu.objects.all()

    context = {'menus': menus}

    return render(request, 'app/admin_menu.html', context)

def modificarMenu(request, pk):
    menu = Menu.objects.get(id=pk)
    form = MenuForm(instance=menu)

    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('/administrar_menu')

    context = {'form': form, 'menu': menu}
    return render(request, 'app/menu_form.html', context)

def ingresarMenu(request):
    if request.method == 'POST':
        form = IngresarMenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/administrar_menu')
    else:
        form = IngresarMenuForm()
    
    context = {'form': form}
    return render(request, 'app/menu_form.html', context)

### ADMIN COMERCIO ###
def administrarComercio(request):
    comercios = Comercio.objects.all()

    context = {'comercios': comercios}

    return render(request, 'app/admin_comercio.html', context)

def modificarComercio(request, pk):
    comercio = Comercio.objects.get(id=pk)
    form = ComercioForm(instance=comercio)

    if request.method == 'POST':
        form = ComercioForm(request.POST, instance=comercio)
        if form.is_valid():
            form.save()
            return redirect('/administrar_comercio')

    context = {'form': form, 'comercio': comercio}
    return render(request, 'app/comercio_form.html', context)

def ingresarComercio(request):
    if request.method == 'POST':
        form = IngresarComercioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/administrar_comercio')
    else:
        form = IngresarComercioForm()

    context = {'form': form}
    return render(request, 'app/comercio_form.html', context)

def deshabilitarComentario(request, pk):
    comentario = Comentario.objects.get(id=pk)

    if request.method == "POST":
        comentario.is_active = False
        comentario.save()
        return redirect('/')

    context={'comentario': comentario}
    return render(request, 'app/deshabilitar_comentario.html', context)

### VISTAS ###

def vistaMenu(request, pk):
    form = ComentarioForm()
    menu = Menu.objects.get(id=pk)
    comentarios = menu.comentario_set.filter(is_active = True)

    if comentarios:
        calificacion_media = comentarios.aggregate(Avg('calificacion'))
        menu.calificacion_media = round(calificacion_media.get('calificacion__avg'), 1)
        menu.save()
    
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

def buscarMenu(request):
    menus = Menu.objects.filter(comercio__is_active = True, is_active = True)
    searched = ""

    if request.method == "POST":
        searched = request.POST['searched']
        menus = menus.filter(titulo__icontains = searched)

    myFilter = MenuFilter(request.GET, queryset=menus)
    menus = myFilter.qs

    context = {'menus': menus, 'myFilter': myFilter, 'searched': searched}

    return render(request, 'app/buscar_menu.html', context)

def vistaComercio(request, pk):
    comercio = Comercio.objects.get(id=pk)
    menus = comercio.menu_set.filter(is_active = True)

    context = { 'comercio': comercio, 'menus': menus}

    return render(request, "app/comercio.html", context)