from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public_pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('citoyen/', include('demandes.urls')),
    path('admin-espace/', include('services.urls')),
    path('paiements/', include('paiements.urls')),
    path('reclamations/', include('reclamations.urls')),
    path('notifications/', include('notifications.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
