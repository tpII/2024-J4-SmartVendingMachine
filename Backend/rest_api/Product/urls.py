# creditcards/urls.py
from django.urls import path
from .views import *
urlpatterns = [
    path('create-product/', ProductCreateView().as_view(), name='product_create'),
    path('delete-product/<int:pk>/', DeleteProductView.as_view(), name='delete_product'),
    path('check-stock/', CheckStock.as_view(), name='check_product_stock'),

]