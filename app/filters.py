import django_filters
from django_filters import CharFilter

from .models import *

class MenuFilter(django_filters.FilterSet):

    class Meta:
        model = Menu
        fields = '__all__'
        exclude = ['titulo','descripcion', 'menu_pic', 'is_active']