from django.contrib import admin
from .models import Reclamation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    readonly_fields = ['date_envoi']

@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ['numero_ticket', 'citoyen', 'sujet', 'categorie', 'statut', 'date_creation']
    list_filter = ['statut', 'categorie']
    search_fields = ['numero_ticket', 'sujet', 'citoyen__user__first_name', 'citoyen__user__last_name']
    inlines = [MessageInline]
    readonly_fields = ['numero_ticket', 'date_creation', 'date_mise_a_jour']
