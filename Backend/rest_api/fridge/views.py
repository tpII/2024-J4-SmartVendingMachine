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
#   
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
