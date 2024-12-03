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
        # Verificar si el usuario ya tiene otras tarjetas
        has_other_cards = CreditCard.objects.filter(user=request.user).exists()
        
        favourite_value = not has_other_cards
        data = request.data.copy()
        data['favourite'] = not has_other_cards  # True si no tiene otras tarjetas, False en caso contrario
        
        # Crear el serializador con los datos de la solicitud
        serializer = CreditCardSerializer(data=data)
        if serializer.is_valid():
            # Asignar `favourite` automticamente sin depender de la solicitud
            credit_card = serializer.save(user=request.user, favourite=favourite_value)
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


class AddFavouriteCardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Obtener el ID de la tarjeta desde los datos de la solicitud
        card_id = request.data.get('id')
        if not card_id:
            return Response({'error': 'No ID provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verificar que la tarjeta pertenece al usuario autenticado
            card_to_favourite = CreditCard.objects.get(id=card_id, user=request.user)
            
            # Desactivar 'favourite' en todas las otras tarjetas del usuario
            CreditCard.objects.filter(user=request.user).update(favourite=False)
            
            # Activar 'favourite' en la tarjeta especificada
            card_to_favourite.favourite = True
            card_to_favourite.save()
            
            # Serializar y devolver las tarjetas actualizadas del usuario
            user_credit_cards = CreditCard.objects.filter(user=request.user)
            serializer = CreditCardSerializer(user_credit_cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except CreditCard.DoesNotExist:
            return Response({'error': 'Card not found or does not belong to user'}, status=status.HTTP_404_NOT_FOUND)
