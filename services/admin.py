from django.contrib import admin
from .models import ServiceAdministratif


@admin.register(ServiceAdministratif)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'tarif', 'delai_jours', 'actif']
    list_filter = ['categorie', 'actif']
    search_fields = ['nom', 'description']
    list_editable = ['tarif', 'delai_jours', 'actif']
