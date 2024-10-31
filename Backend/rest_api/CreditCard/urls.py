# creditcards/urls.py
from django.urls import path
from .views import CreditCardCreateView, CreditCardDeleteView

urlpatterns = [
    path('api/credit-card/', CreditCardCreateView.as_view(), name='credit_card_create'),
    path('api/credit-card/<int:pk>/', CreditCardDeleteView.as_view(), name='credit_card_delete'),
]
