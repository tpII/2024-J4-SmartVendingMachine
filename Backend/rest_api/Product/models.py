from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Product(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    en_heladera = models.BooleanField(default=False)  # Si est o no en la heladera
    

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"