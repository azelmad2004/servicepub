from django.urls import path

from . import views

urlpatterns = [
    path("<int:demande_id>/", views.paiement, name="paiement"),
    path("<int:demande_id>/recapitulatif/", views.recapitulatif, name="recapitulatif"),
]
