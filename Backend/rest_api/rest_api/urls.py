from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("authentication.urls")),
    path("market/", include("fridge.urls")),
    path("payment/", include("CreditCard.urls"))
]

if settings.DEBUG:  # Solo servir en modo desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)