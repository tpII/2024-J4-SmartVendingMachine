from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'en_heladera']
    list_filter = ['en_heladera']