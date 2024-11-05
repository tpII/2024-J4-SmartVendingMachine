# creditcards/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('create-card/', CreditCardCreateView.as_view(), name='credit_card_create'),
    path('delete-card/<int:pk>/', CreditCardDeleteView.as_view(), name='credit_card_delete'),
    path('check-card/', HasCreditCardView.as_view(), name='has_credit_card'),
    path('credit-cards/', AllCreditCardsView.as_view(), name='user_credit_cards'),
    path('credit-cards/add-favourite/', AddFavouriteCardView.as_view(), name='user_add_fav_credit_card')
]
