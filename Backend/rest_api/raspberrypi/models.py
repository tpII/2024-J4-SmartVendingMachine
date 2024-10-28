from django.db import models
from .models import Heladera

class RaspberryPi(models.Model):
    identificador = models.CharField(max_length=100, unique=True)
    heladera = models.ForeignKey(Heladera, on_delete=models.CASCADE)
    secreto = models.CharField(max_length=255)

    def __str__(self):
        return f"Raspberry Pi {self.identificador}"
