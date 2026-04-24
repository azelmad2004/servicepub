from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_reclamations_citoyen, name='liste_reclamations_citoyen'),
    path('nouvelle/', views.nouvelle_reclamation, name='nouvelle_reclamation'),
    path('<int:rec_id>/', views.detail_reclamation, name='detail_reclamation'),
    path('admin/', views.admin_reclamations, name='admin_reclamations'),
    path('admin/<int:rec_id>/', views.admin_repondre_reclamation, name='admin_repondre_reclamation'),
]
