from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Estudiante(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length = 254)
    profile_pic  = models.ImageField(default="default-profile-pic.png",null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username

class Comercio(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    descripcion = models.CharField(max_length=500, null=True)
    direccion = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre

class Menu(models.Model):
    comercio = models.ForeignKey(Comercio, null=True, on_delete=models.SET_NULL)
    
    titulo = models.CharField(max_length=100, null=True)
    precio = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=500, null=True)
    calificacion_media = models.FloatField(default=0)
    menu_pic  = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    categoria = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    menu = models.ForeignKey(Menu, null=True,on_delete=models.SET_NULL)
    estudiante = models.ForeignKey(Estudiante, null=True,on_delete=models.SET_NULL)

    contenido = models.CharField(max_length=500, null=True)
    calificacion = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

class Recomendacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, null=True,on_delete=models.SET_NULL)

    nombre = models.CharField(max_length=100, null=True)
    contenido = models.CharField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo