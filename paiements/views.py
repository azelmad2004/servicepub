from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Paiement


@login_required
def paiement(request, demande_id):
    if not hasattr(request.user, 'profil_citoyen'):
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    citoyen = request.user.profil_citoyen
    from demandes.models import Demande
    demande = get_object_or_404(Demande, id=demande_id, citoyen=citoyen)
    paiement_obj = get_object_or_404(Paiement, demande=demande)
    if request.method == 'POST':
        methode = request.POST.get('methode', 'carte')
        paiement_obj.methode = methode
        paiement_obj.statut = 'paye'
        paiement_obj.date_paiement = timezone.now()
        paiement_obj.transaction_id = f"TXN-{demande.reference}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        paiement_obj.save()
        demande.statut = 'en_traitement'
        demande.save()
        messages.success(request, f"Paiement de {paiement_obj.montant} MAD confirmé !")
        return redirect('detail_demande', demande_id=demande.id)
    return render(request, 'paiements/paiement.html', {
        'demande': demande,
        'paiement': paiement_obj,
    })


@login_required
def recapitulatif(request, demande_id):
    if not hasattr(request.user, 'profil_citoyen'):
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    citoyen = request.user.profil_citoyen
    from demandes.models import Demande
    demande = get_object_or_404(Demande, id=demande_id, citoyen=citoyen)
    return render(request, 'paiements/recapitulatif.html', {'demande': demande})
