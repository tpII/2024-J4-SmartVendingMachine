from django.contrib import admin
from .models import CreditCard

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_holder_name', 'masked_card_number', 'expiration_date')
    
    def masked_card_number(self, obj):
        # Muestra solo los últimos 4 dgitos del número de la tarjeta
        return f"**** **** **** {obj.card_number[-4:]}"
    masked_card_number.short_description = 'Card Number'