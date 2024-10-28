from rest_framework import serializers
from .models import *

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'foto', 'precio', 'cantidad']

class HeladeraSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Heladera
        fields = ['id', 'latitud', 'longitud', 'productos']

class ProductoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoCompra
        fields = ['producto', 'cantidad']

class SesionCompraSerializer(serializers.ModelSerializer):
    productos = ProductoCompraSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = SesionCompra
        fields = ['usuario', 'heladera', 'fecha_inicio', 'productos']

    def create(self, validated_data):
        sesion = SesionCompra.objects.create(**validated_data)
        return sesion
