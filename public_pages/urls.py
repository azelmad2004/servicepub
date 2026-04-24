from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fonctionnalites/', views.fonctionnalites, name='fonctionnalites'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('contact/', views.contact, name='contact'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('faq/', views.faq, name='faq'),
    path('cgu/', views.cgu, name='cgu'),
    path('confidentialite/', views.confidentialite, name='confidentialite'),
    path('cookies/', views.cookies, name='cookies'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
]
