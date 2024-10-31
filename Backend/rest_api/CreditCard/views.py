from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CreditCard
from .serializers import CreditCardSerializer
from django.core.exceptions import ValidationError

class CreditCardCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validar que el usuario tenga al menos una tarjeta después de crearla
        serializer = CreditCardSerializer(data=request.data)
        if serializer.is_valid():
            credit_card = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)