# creditcards/urls.py
from django.urls import path
from .views import CreditCardCreateView, CreditCardDeleteView
from .views import HasCreditCardView

urlpatterns = [
    path('create-card/', CreditCardCreateView.as_view(), name='credit_card_create'),
    path('delete-card/<int:pk>/', CreditCardDeleteView.as_view(), name='credit_card_delete'),
    path('check-card/', HasCreditCardView.as_view(), name='has_credit_card')
]
