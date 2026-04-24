from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription_citoyen, name='inscription_citoyen'),
    path('inscription-admin/', views.inscription_admin, name='inscription_admin'),
    path('connexion/', views.connexion_citoyen, name='connexion_citoyen'),
    path('connexion-admin/', views.connexion_admin, name='connexion_admin'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie, name='mot_de_passe_oublie'),
    path('profil/', views.profil_citoyen, name='profil_citoyen'),
]
