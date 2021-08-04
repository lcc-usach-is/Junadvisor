from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('ingresar_menu/', views.ingresarMenu, name="ingresar_menu"),
]