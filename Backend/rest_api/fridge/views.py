from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

# Esta vista devuelve los productos que estan almacenados en una heladera
# en conjunto con su id, latitud y longitud.
#   .Tom
class HeladeraDetailView(generics.RetrieveAPIView):
    queryset = Heladera.objects.all()
    serializer_class = HeladeraSerializer

#  Esta vista crea un objeto "sesion" en la base de datos. Cada sesion es una sesion de compras
#  a la cual se le asocia un usuario, una raspberry, uno/unos serie de productos. La sesion 
#   .Tom
class StartSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        heladera = Heladera.objects.get(id=id)
        data = request.data.copy()
        data['heladera'] = heladera.id
        data['usuario'] = request.user.id

        serializer = SesionCompraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#   Esta vista devuelve en formato de lista simple las heladeras con sus respectivas 
#   ubicaciones en latitud y longitud
#       .Tom
class UbicacionesHeladerasView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def get(self, request):
        heladeras = Heladera.objects.all()
        if not heladeras.exists():  # Verifica si no hay heladeras
            return Response({"error": "No se encontraron heladeras."}, status=404)

        payload_response = {}
        for heladera in heladeras:
            payload_response[heladera.id] = {
                'lat': heladera.latitud,
                'lng': heladera.longitud
            }

        return Response(payload_response, status=200)

#   Recibe como parametro el id de una heladera
#   y descarga en formato de array los productos que hay en ella
#       .Tom
class ProductListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, heladera_id):
        try:
            # Obtener la heladera por su ID
            heladera = Heladera.objects.get(id=heladera_id)
        except Heladera.DoesNotExist:
            return Response(
                {"error": f"No se encontró la heladera con ID {heladera_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Obtener los productos relacionados con la heladera
        productos = Producto.objects.filter(heladera=heladera)

        # Serializar los datos
        productos_data = [
            {
                "name": producto.nombre, 
                "image": request.build_absolute_uri(producto.foto.url) if producto.foto else None,
                "price": producto.precio
            }
            for producto in productos
        ]

        return Response(productos_data, status=status.HTTP_200_OK)