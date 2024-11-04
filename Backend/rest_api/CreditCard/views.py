from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CreditCard
from .serializers import CreditCardSerializer
from django.core.exceptions import ValidationError

class CreditCardCreateView(APIView):
    

    def post(self, request):
        # Validar que el usuario tenga al menos una tarjeta después de crearla
        serializer = CreditCardSerializer(data=request.data)
        if serializer.is_valid():
            credit_card = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class HasCreditCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        has_card = request.user.credit_cards.exists()
        return Response({'has_card': has_card})
    

class CreditCardDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            credit_card = CreditCard.objects.get(pk=pk, user=request.user)
            if request.user.credit_cards.count() <= 1:
                raise ValidationError("Cannot delete the last credit card. Each user must have at least one associated credit card.")
            credit_card.delete()
            return Response({"message": "Credit card deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except CreditCard.DoesNotExist:
            return Response({"error": "Credit card not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AllCreditCardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obtener todas las tarjetas asociadas al usuario autenticado
        user_credit_cards = CreditCard.objects.filter(user=request.user)
        serializer = CreditCardSerializer(user_credit_cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
