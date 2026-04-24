from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.liste_services, name='liste_services'),
    path('services/gestion/', views.admin_gestion_services, name='admin_gestion_services'),
    path('services/<int:service_id>/toggle/', views.admin_toggle_service, name='admin_toggle_service'),
    path('agents/', views.admin_gestion_agents, name='admin_gestion_agents'),
    path('citoyens/', views.admin_gestion_citoyens, name='admin_gestion_citoyens'),
]
