from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('', views.home, name="home"),
    path('menu/<str:pk>', views.vistaMenu, name="menu"),

    path('ingresar_menu/', views.ingresarMenu, name="ingresar_menu"),
]