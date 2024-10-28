from django.contrib import admin
from .models import Heladera, Producto

@admin.register(Heladera)
class HeladeraAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitud', 'longitud')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'cantidad', 'heladera')
    list_filter = ('heladera',)
