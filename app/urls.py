from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('', views.home, name="home"),
    path('menu/<str:pk>', views.vistaMenu, name="menu"),
    path('comercio/<str:pk>', views.vistaComercio, name="comercio"),

    path('administrar_menu/', views.administrarMenu, name="administrar_menu"),
    path('ingresar_menu/', views.ingresarMenu, name="ingresar_menu"),
    path('modificar_menu/<str:pk>', views.modificarMenu, name="modificar_menu"),
    path('buscar_menu/', views.buscarMenu, name="buscar_menu"),

    path('administrar_comercio/', views.administrarComercio, name="administrar_comercio"),
    path('ingresar_comercio/', views.ingresarComercio, name="ingresar_comercio"),
    path('modificar_comercio/<str:pk>', views.modificarComercio, name="modificar_comercio"),
    
    path('deshabilitar_comentario/<str:pk>', views.deshabilitarComentario, name="deshabilitar_comentario"),
]