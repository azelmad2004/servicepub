from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['demande', 'montant', 'methode', 'statut', 'date_paiement', 'transaction_id']
    list_filter = ['statut', 'methode']
    search_fields = ['demande__reference', 'transaction_id']
    readonly_fields = ['date_creation']
