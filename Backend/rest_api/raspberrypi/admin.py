from django.contrib import admin
from .models import RaspberryPi

@admin.register(RaspberryPi)
class RaspberryPiAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'heladera')
