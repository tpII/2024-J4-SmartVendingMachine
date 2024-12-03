from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404


class ProductCreateView(APIView):

    permission_classes = [IsAuthenticated] 

    
    def post(self, request):
        # Validar que el usuario tenga al menos una tarjeta despus de crearla
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ToggleEnHeladeraView(APIView):
    permission_classes = [IsAuthenticated]  # Asegura que solo usuarios autenticados puedan cambiar el estado

    def patch(self, request, pk):
        # Obtn el producto por su ID (pk) o devuelve 404 si no se encuentra
        producto = get_object_or_404(Product, pk=pk)
        
        # Cambia el estado de en_heladera
        producto.en_heladera = not producto.en_heladera
        producto.save()
        
        # Serializa y retorna el producto actualizado
        serializer = ProductSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]  # Asegura que solo usuarios autenticados puedan eliminar

    def delete(self, request, pk):
        # Obtn el producto por su ID (pk) o devuelve 404 si no se encuentra
        producto = get_object_or_404(Product, pk=pk)
        
        # Elimina el producto
        producto.delete()
        
        # Retorna una respuesta de xito
        return Response({"message": "Producto eliminado exitosamente"}, status=status.HTTP_204_NO_CONTENT)

class CheckStock(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        producto = get_object_or_404(Product, pk=pk)
        # Devuelve el estado de en_heladera para verificar si el producto est en stock
        return Response({"en_heladera": producto.en_heladera}, status=status.HTTP_200_OK)