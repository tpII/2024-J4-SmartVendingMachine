# creditcards/urls.py
from django.urls import path
from .views import CreditCardCreateView, CreditCardDeleteView
from .views import HasCreditCardView
from .views import AllCreditCardsView

urlpatterns = [
    path('create-card/', CreditCardCreateView.as_view(), name='credit_card_create'),
    path('delete-card/<int:pk>/', CreditCardDeleteView.as_view(), name='credit_card_delete'),
    path('check-card/', HasCreditCardView.as_view(), name='has_credit_card'),
    path('credit-cards/', AllCreditCardsView.as_view(), name='user_credit_cards')

]
