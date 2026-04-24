from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Citoyen, AgentAdministratif


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('ServicePub', {'fields': ('role', 'telephone', 'adresse')}),
    )


@admin.register(Citoyen)
class CitoyenAdmin(admin.ModelAdmin):
    list_display = ['user', 'CINE', 'lieu_naissance', 'date_inscription', 'actif']
    list_filter = ['actif']
    search_fields = ['user__first_name', 'user__last_name', 'CINE', 'user__email']
    date_hierarchy = 'date_inscription'


@admin.register(AgentAdministratif)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'administration', 'poste', 'actif']
    list_filter = ['actif', 'administration']
    search_fields = ['user__first_name', 'user__last_name', 'administration']
