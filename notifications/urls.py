from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_notifications, name='liste_notifications'),
    path('<int:notif_id>/lue/', views.marquer_lue, name='marquer_lue'),
    path('toutes-lues/', views.marquer_toutes_lues, name='marquer_toutes_lues'),
    path('api/count/', views.count_non_lues, name='count_non_lues'),
]
