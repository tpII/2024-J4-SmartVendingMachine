from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class CreditCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_cards')
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)
    card_holder_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.card_holder_name} - {self.card_number[-4:]}"

# Signal to ensure at least one credit card is associated with each user

