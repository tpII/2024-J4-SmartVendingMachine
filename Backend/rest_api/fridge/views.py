from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .utils.ZMQconection import ZMQConnection, ZMQClient
from .utils.message_codec import MessageCodec

# Instancia de ZMQConnection
zmq_client = ZMQClient()

products=""
# Instancia de Decodificador
codec = MessageCodec()

# Vista para obtener detalles de una heladera
class HeladeraDetailView(generics.RetrieveAPIView):
    queryset = Heladera.objects.all()
    serializer_class = HeladeraSerializer

# Vista para iniciar una sesión de compra
class StartSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        # Conexión ZMQ para enviar mensajes
        heladera = Heladera.objects.get(id=id)
        data = request.data.copy()
        data['heladera'] = heladera.id
        data['usuario'] = request.user.id
        
        # Enviar mensaje a la Raspberry
        try:
            zmq_client.send_message('start')
        except RuntimeError as e:
            return Response({"error": f"Error al enviar mensaje: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serializar los datos de la sesión
        serializer = SesionCompraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para obtener los mensajes recibidos desde la Raspberry
class ReceivedMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Devuelve los mensajes recibidos desde la Raspberry.
        """
        messages = zmq_client.get_received_messages()
        return Response({"messages": messages}, status=status.HTTP_200_OK)

# Vista para obtener las ubicaciones de las heladeras
class UbicacionesHeladerasView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        heladeras = Heladera.objects.all()
        if not heladeras.exists():
            return Response({"error": "No se encontraron heladeras."}, status=404)

        payload_response = {
            heladera.id: {'lat': heladera.latitud, 'lng': heladera.longitud}
            for heladera in heladeras
        }
        return Response(payload_response, status=200)

# Vista para obtener productos de una heladera
class ProductListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, heladera_id):
        try:
            heladera = Heladera.objects.get(id=heladera_id)
        except Heladera.DoesNotExist:
            return Response(
                {"error": f"No se encontró la heladera con ID {heladera_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        productos = Producto.objects.filter(heladera=heladera)
        productos_data = [
            {
                "name": producto.nombre,
                "image": request.build_absolute_uri(producto.foto.url) if producto.foto else None,
                "price": producto.precio
            }
            for producto in productos
        ]
        return Response(productos_data, status=status.HTTP_200_OK)

class EndSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        try:
            # Recuperar información de los productos desde la sesión
            productos_info = request.session.get('productos_info', None)
            print(productos_info)
            if not productos_info:
                return Response(
                    {"error": "No se encontraron productos procesados para esta sesión."},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({"productos_info": productos_info}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al obtener los productos: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id):
        # Conexión ZMQ para enviar mensajes
        heladera = Heladera.objects.get(id=id)
        data = request.data.copy()
        data['heladera'] = heladera.id
        data['usuario'] = request.user.id
        
        # Enviar mensaje a la Raspberry
        try:
            zmq_client.send_message('stop')
        except RuntimeError as e:
            return Response({"error": f"Error al enviar mensaje: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            respuesta_rpi = zmq_client.wait_for_message()
        except:
            return Response({"error": f"Error al recibir el mensaje"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Decodificamos el mensaje
        products = codec.decode(respuesta_rpi)
        print(products)

        productos_info = {}
        
        try:
            for name, cantidad_retirada in products.items():
                # Buscar el producto por su nombre y asociarlo a la heladera
                producto = Producto.objects.filter(nombre=name, heladera=1).first()
                
                if not producto:
                    return Response(
                        {"error": f"Producto '{name}' no encontrado en esta heladera."},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                productos_info[name] = {
                    'precio': float(producto.precio),
                    'stock_anterior': producto.cantidad,
                    'cantidad_retirada': cantidad_retirada,
                    'stock_actual': producto.cantidad - cantidad_retirada if producto.cantidad >= cantidad_retirada else 0
                }
                print(name)
                print(productos_info[name])
        except Exception as e:
            return Response({"error": f"Error procesando productos: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        request.session['productos_info'] = productos_info
        request.session.modified = True

        # Serializar los datos de la sesión
        serializer = SesionCompraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                    'sesion': serializer.data,
                    'productos_info': productos_info
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
