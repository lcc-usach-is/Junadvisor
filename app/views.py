from app.forms import MenuForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *

# Create your views here.

def home(request):
    return render(request, 'app/dashboard.html')

def ingresarMenu(request):
    form = MenuForm()

    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
            
    context = {'form': form}
    return render(request, 'app/menu_form.html', context)