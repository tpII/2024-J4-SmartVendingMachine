from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RaspberryPi, SesionCompra, ProductoCompra, Producto
from .serializers import RaspberryPiSerializer

class RaspberryPiSessionView(APIView):
    def post(self, request):
        data = request.data
        raspberry_id = data.get("raspberry-id")
        secret = data.get("secret")
        session_id = data.get("session-id")
        product_ids = data.get("products", [])

        # Verificar la existencia y el secreto de Raspberry Pi
        try:
            raspberry = RaspberryPi.objects.get(identificador=raspberry_id)
            if raspberry.secreto != secret:
                return Response({"detail": "Acceso denegado: secreto incorrecto"}, status=status.HTTP_403_FORBIDDEN)
        except RaspberryPi.DoesNotExist:
            return Response({"detail": "Raspberry Pi no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        # Verificar la existencia de la sesión de compra
        try:
            session = SesionCompra.objects.get(id=session_id)
        except SesionCompra.DoesNotExist:
            return Response({"detail": "Sesión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        # Agregar productos a la sesión
        for product_id in product_ids:
            try:
                producto = Producto.objects.get(id=product_id)
                ProductoCompra.objects.create(sesion=session, producto=producto, cantidad=1)  # Asume cantidad = 1
            except Producto.DoesNotExist:
                return Response({"detail": f"Producto {product_id} no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Cambiar el estado de la sesión a false (cerrada)
        session.estado = False
        session.save()

        return Response({"detail": "Productos añadidos y sesión actualizada"}, status=status.HTTP_200_OK)
