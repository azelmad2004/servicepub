from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['destinataire', 'titre', 'type_notif', 'lue', 'date_envoi']
    list_filter = ['type_notif', 'lue']
    search_fields = ['destinataire__username', 'titre', 'contenu']
    readonly_fields = ['date_envoi']
