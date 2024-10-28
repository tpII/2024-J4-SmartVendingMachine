from django.urls import path
from .views import *

urlpatterns = [
    path('fridge/raspberry-session/', RaspberryPiSessionView.as_view(), name='raspberry-session'),
]
