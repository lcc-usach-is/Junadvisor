from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Comercio)
admin.site.register(Categoria)
admin.site.register(Menu)