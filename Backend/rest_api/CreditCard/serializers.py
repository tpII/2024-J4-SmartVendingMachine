from rest_framework import serializers
from .models import CreditCard

class CreditCardSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateField(format="%Y-%m", input_formats=["%Y-%m"])

    class Meta:
        model = CreditCard
        fields = ['id', 'user', 'card_number', 'expiration_date', 'cvv', 'card_holder_name', 'favourite']
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['card_number'] = "**** **** **** " + instance.card_number[-4:]
        return representation
