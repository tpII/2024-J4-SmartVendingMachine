from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','nombre', 'precio', 'en_heladera']  # Campos incluidos en el serializador

