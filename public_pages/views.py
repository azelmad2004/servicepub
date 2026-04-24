from django.shortcuts import render
from django.utils import timezone
from services.models import ServiceAdministratif
from accounts.models import Citoyen
from demandes.models import Demande


def index(request):
    stats = {
        'citoyens': Citoyen.objects.count() or 500,
        'demandes': Demande.objects.count() or 1200,
        'services': ServiceAdministratif.objects.filter(actif=True).count() or 12,
    }
    return render(request, 'public_pages/index.html', {'stats': stats})


def fonctionnalites(request):
    return render(request, 'public_pages/Fonctionalites.html')


def statistiques(request):
    stats = {
        'citoyens': Citoyen.objects.count() or 500,
        'demandes': Demande.objects.count() or 1200,
        'traitees': Demande.objects.filter(statut='traitee').count() or 980,
        'services': ServiceAdministratif.objects.filter(actif=True).count() or 12,
    }
    return render(request, 'public_pages/Statistiques.html', {'stats': stats})


def contact(request):
    sent = False
    if request.method == 'POST':
        sent = True
    return render(request, 'public_pages/Contact.html', {'sent': sent})


def a_propos(request):
    return render(request, 'public_pages/a_propos.html')


def faq(request):
    faqs = [
        {"q": "Comment créer une demande ?", "r": "Connectez-vous, allez dans 'Nouvelle Demande', choisissez votre service et suivez les étapes."},
        {"q": "Quels documents sont nécessaires ?", "r": "Chaque service précise les documents requis lors de la sélection."},
        {"q": "Comment suivre ma demande ?", "r": "Dans votre espace citoyen, section 'Mes Demandes', vous trouverez le statut en temps réel."},
        {"q": "Combien de temps prend le traitement ?", "r": "Le délai varie selon le service, de 2 à 10 jours ouvrables."},
        {"q": "Comment payer les frais ?", "r": "Le paiement s'effectue en ligne par carte bancaire ou CMI après création de la demande."},
        {"q": "Puis-je annuler une demande ?", "r": "Oui, tant que la demande est en statut 'En cours', avant le début du traitement."},
    ]
    return render(request, 'public_pages/faq.html', {'faqs': faqs})


def cgu(request):
    return render(request, 'public_pages/cgu.html', {'today': timezone.now()})


def confidentialite(request):
    return render(request, 'public_pages/Confidentialite.html', {'today': timezone.now()})


def cookies(request):
    return render(request, 'public_pages/Cookies.html', {'today': timezone.now()})


def mentions_legales(request):
    return render(request, 'public_pages/Mentions.html', {'today': timezone.now()})
