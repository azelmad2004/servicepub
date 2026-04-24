from django.contrib import admin
from .models import Demande, Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ['date_upload']


@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ['reference', 'citoyen', 'service', 'statut', 'date_creation', 'date_echeance', 'agent']
    list_filter = ['statut', 'service__categorie']
    search_fields = ['reference', 'citoyen__user__first_name', 'citoyen__user__last_name', 'citoyen__CINE']
    date_hierarchy = 'date_creation'
    readonly_fields = ['reference', 'date_creation']
    inlines = [DocumentInline]
    actions = ['marquer_traitee', 'marquer_livree']

    @admin.action(description='Marquer comme traitée')
    def marquer_traitee(self, request, queryset):
        queryset.update(statut='traitee')

    @admin.action(description='Marquer comme livrée')
    def marquer_livree(self, request, queryset):
        queryset.update(statut='livree')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['titre', 'demande', 'type_doc', 'valide', 'date_upload']
    list_filter = ['type_doc', 'valide']
