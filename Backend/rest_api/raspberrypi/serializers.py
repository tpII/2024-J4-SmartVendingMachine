from rest_framework import serializers
from .models import RaspberryPi

class RaspberryPiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaspberryPi
        fields = ['identificador', 'heladera', 'secreto']
        extra_kwargs = {'secreto': {'write_only': True}}
