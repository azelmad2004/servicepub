from django.urls import path
from . import views

urlpatterns = [
    # Citoyen
    path('dashboard/', views.citoyen_dashboard, name='citoyen_dashboard'),
    path('demandes/', views.liste_demandes, name='liste_demandes'),
    path('demandes/nouvelle/', views.nouvelle_demande, name='nouvelle_demande'),
    path('demandes/service/<int:service_id>/', views.choisir_service, name='choisir_service'),
    path('demandes/<int:demande_id>/', views.detail_demande, name='detail_demande'),
    path('demandes/<int:demande_id>/documents/', views.upload_documents, name='upload_documents'),
    path('demandes/<int:demande_id>/recapitulatif/', views.recapitulatif, name='recapitulatif'),
    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/demandes/', views.admin_demandes, name='admin_demandes'),
    path('admin/demandes/<int:demande_id>/traiter/', views.admin_traiter_demande, name='admin_traiter_demande'),
    path('admin/activer-agent/<int:agent_id>/', views.admin_activer_agent, name='admin_activer_agent'),
    path('admin/agents/', views.admin_dashboard, name='admin_gestion_agents'), # Redirect to dashboard for now
]
