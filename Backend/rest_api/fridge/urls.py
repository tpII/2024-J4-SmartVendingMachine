from django.urls import path
from .views import *

urlpatterns = [
    path('fridge/geolocations/', UbicacionesHeladerasView.as_view(), name='heladera-geolocation'),
    path('fridge/<int:pk>/', HeladeraDetailView.as_view(), name='heladera-detail'),
    path('fridge/start-session/<int:id>/', StartSessionView.as_view(), name='start-session'),
    path("fridge/<int:heladera_id>/products/list/", ProductListView.as_view(), name="product-list"),
]
