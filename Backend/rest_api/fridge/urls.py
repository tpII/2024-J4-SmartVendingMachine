from django.urls import path
from .views import *

urlpatterns = [
    path('fridge/<int:pk>/', HeladeraDetailView.as_view(), name='heladera-detail'),
    path('fridge/start-session/<int:id>/', StartSessionView.as_view(), name='start-session'),
]
