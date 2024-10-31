from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("authentication.urls")),
    path("market/", include("fridge.urls")),
    path("payment/", include("CreditCard.urls"))
]
