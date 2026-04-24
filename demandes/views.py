from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Demande, Document
from .forms import NouvelleDemandeForm, DocumentUploadForm
from services.models import ServiceAdministratif
from paiements.models import Paiement
from notifications.models import Notification


def _get_citoyen(request):
    try:
        return request.user.profil_citoyen
    except AttributeError:
        return None


@login_required
def citoyen_dashboard(request):
    citoyen = _get_citoyen(request)
    if not citoyen:
        if request.user.role in ['admin', 'agent']:
            return redirect('admin_dashboard')
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')

    demandes_recentes = Demande.objects.filter(citoyen=citoyen).order_by('-date_creation')[:5]
    notifs = Notification.objects.filter(destinataire=request.user, lue=False).order_by('-date_envoi')[:5]
    notifs_count = Notification.objects.filter(destinataire=request.user, lue=False).count()
    stats = {
        'total': Demande.objects.filter(citoyen=citoyen).count(),
        'en_cours': Demande.objects.filter(citoyen=citoyen, statut__in=['en_cours', 'en_traitement']).count(),
        'traitees': Demande.objects.filter(citoyen=citoyen, statut='traitee').count(),
        'livrees': Demande.objects.filter(citoyen=citoyen, statut='livree').count(),
    }
    context = {
        'citoyen': citoyen,
        'demandes_recentes': demandes_recentes,
        'notifications': notifs,
        'notifications_count': notifs_count,
        'stats': stats,
    }
    return render(request, 'demandes/dashboard-citoyen.html', context)


@login_required
def liste_demandes(request):
    citoyen = _get_citoyen(request)
    if not citoyen:
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    statut_filtre = request.GET.get('statut', '')
    demandes = Demande.objects.filter(citoyen=citoyen)
    if statut_filtre:
        demandes = demandes.filter(statut=statut_filtre)
    context = {
        'demandes': demandes,
        'statut_filtre': statut_filtre,
        'statuts': Demande.STATUT_CHOICES,
    }
    return render(request, 'demandes/demandes-citoyen.html', context)


@login_required
def nouvelle_demande(request):
    if not hasattr(request.user, 'profil_citoyen'):
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    services = ServiceAdministratif.objects.filter(actif=True).order_by('categorie')
    services_par_categorie = {}
    for s in services:
        cat = s.get_categorie_display()
        services_par_categorie.setdefault(cat, []).append(s)
    return render(request, 'demandes/nouvelle-demande.html', {
        'services_par_categorie': services_par_categorie
    })


@login_required
def choisir_service(request, service_id):
    if not hasattr(request.user, 'profil_citoyen'):
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    service = get_object_or_404(ServiceAdministratif, id=service_id, actif=True)
    if request.method == 'POST':
        form = NouvelleDemandeForm(request.POST)
        if form.is_valid():
            citoyen = _get_citoyen(request)
            demande = form.save(commit=False)
            demande.citoyen = citoyen
            demande.service = service
            demande.date_echeance = (timezone.now() + timedelta(days=service.delai_jours)).date()
            demande.save()
            Paiement.objects.create(demande=demande, montant=service.tarif)
            Notification.objects.create(
                destinataire=request.user,
                titre="Demande créée",
                contenu=f"Votre demande {demande.reference} a été enregistrée.",
                type_notif='succes',
                lien=f'/citoyen/demandes/{demande.id}/',
            )
            messages.success(request, f"Demande {demande.reference} créée ! Ajoutez vos pièces justificatives.")
            return redirect('upload_documents', demande_id=demande.id)
    else:
        form = NouvelleDemandeForm()
    return render(request, 'demandes/formulaire-demande-passeport.html', {'service': service, 'form': form})


@login_required
def detail_demande(request, demande_id):
    citoyen = _get_citoyen(request)
    if not citoyen:
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    demande = get_object_or_404(Demande, id=demande_id, citoyen=citoyen)
    return render(request, 'demandes/historique-demande.html', {'demande': demande})


@login_required
def upload_documents(request, demande_id):
    citoyen = _get_citoyen(request)
    if not citoyen:
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    demande = get_object_or_404(Demande, id=demande_id, citoyen=citoyen)
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.demande = demande
            doc.save()
            messages.success(request, "Document ajouté avec succès.")
            return redirect('upload_documents', demande_id=demande.id)
    else:
        form = DocumentUploadForm()
    return render(request, 'demandes/upload-documents-demande.html', {'demande': demande, 'form': form})


from fpdf import FPDF
from django.core.files.base import ContentFile
from accounts.models import AgentAdministratif

@login_required
def recapitulatif(request, demande_id):
    citoyen = _get_citoyen(request)
    if not citoyen:
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    
    demande = get_object_or_404(Demande, id=demande_id, citoyen=citoyen)
    
    # Check if a receipt already exists to avoid duplicates
    has_receipt = demande.documents.filter(titre="Reçu de Demande").exists()
    
    if not has_receipt:
        # Assign to first available AgentAdministratif
        agent = AgentAdministratif.objects.first()
        if agent:
            demande.agent = agent
        
        # Update status
        demande.statut = 'en_attente_docs'
        demande.save()
        
        # Generate PDF receipt using fpdf2
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, txt="Reçu de Demande - ServicePub", new_x="LMARGIN", new_y="NEXT", align='C')
        
        pdf.set_font("helvetica", size=12)
        pdf.cell(0, 10, txt=f"Reference: {demande.reference}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 10, txt=f"Citoyen: {demande.citoyen.user.get_full_name()}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 10, txt=f"Service: {demande.service.nom}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 10, txt=f"Date: {demande.date_creation.strftime('%d/%m/%Y')}", new_x="LMARGIN", new_y="NEXT")
        
        # Output as bytes
        pdf_bytes = pdf.output()
        
        # Save to Demande
        doc = Document(
            demande=demande,
            titre="Reçu de Demande",
            type_doc='officiel'
        )
        doc.fichier.save(f"recu_{demande.reference}.pdf", ContentFile(pdf_bytes))
        doc.save()
        
    return render(request, 'demandes/confirmation-demande.html', {'demande': demande})


# ─── Admin views ──────────────────────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    if request.user.role not in ['agent', 'admin']:
        messages.error(request, "Accès refusé.")
        return redirect('index')
    stats = {
        'demandes_total': Demande.objects.count(),
        'en_cours': Demande.objects.filter(statut__in=['en_cours', 'en_traitement']).count(),
        'traitees': Demande.objects.filter(statut='traitee').count(),
        'livrees': Demande.objects.filter(statut='livree').count(),
        'reclamations': 0, # Should be count() from Reclamation model
        'citoyens': 0, # Should be count() from Citoyen model
    }
    from reclamations.models import Reclamation
    from accounts.models import Citoyen, AgentAdministratif
    stats['reclamations'] = Reclamation.objects.count()
    stats['citoyens'] = Citoyen.objects.count()
    demandes_urgentes = Demande.objects.filter(
        statut__in=['en_cours', 'en_traitement'],
        date_echeance__lte=(timezone.now() + timedelta(days=2)).date()
    ).order_by('date_echeance')[:5]
    agents_en_attente = AgentAdministratif.objects.filter(user__is_active=False)[:5]
    context = {
        'stats': stats, 
        'demandes_urgentes': demandes_urgentes,
        'agents_en_attente': agents_en_attente,
    }
    return render(request, 'demandes/admin/dashboard-admin.html', context)


@login_required
def admin_activer_agent(request, agent_id):
    if request.user.role != 'admin':
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('admin_dashboard')
    from accounts.models import AgentAdministratif
    agent = get_object_or_404(AgentAdministratif, id=agent_id)
    agent.user.is_active = True
    agent.user.save()
    messages.success(request, f"Le compte de l'agent {agent.user.get_full_name()} a été activé.")
    return redirect('admin_dashboard')



@login_required
def admin_demandes(request):
    if request.user.role not in ['agent', 'admin']:
        return redirect('index')
    statut_filtre = request.GET.get('statut', '')
    demandes = Demande.objects.all().select_related('citoyen__user', 'service', 'agent__user')
    if statut_filtre:
        demandes = demandes.filter(statut=statut_filtre)
    return render(request, 'demandes/admin/demandes-admin.html', {
        'demandes': demandes,
        'statuts': Demande.STATUT_CHOICES,
        'statut_filtre': statut_filtre,
    })


@login_required
def admin_traiter_demande(request, demande_id):
    if request.user.role not in ['agent', 'admin']:
        return redirect('index')
    demande = get_object_or_404(Demande, id=demande_id)
    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        notes = request.POST.get('notes_agent', '')
        fichier_officiel = request.FILES.get('document_officiel')

        if nouveau_statut in dict(Demande.STATUT_CHOICES):
            demande.statut = nouveau_statut
            demande.notes_agent = notes
            if nouveau_statut == 'traitee':
                demande.date_traitement = timezone.now()
            demande.save()

            if fichier_officiel:
                Document.objects.create(
                    demande=demande,
                    titre=f"Document Officiel - {demande.reference}",
                    type_doc='officiel',
                    fichier=fichier_officiel,
                    valide=True
                )

            Notification.objects.create(
                destinataire=demande.citoyen.user,
                titre=f"Mise à jour — {demande.reference}",
                contenu=f"Votre demande est maintenant : {demande.get_statut_display()}",
                type_notif='info',
                lien=f'/citoyen/demandes/{demande.id}/',
            )
            messages.success(request, "Demande mise à jour et document envoyé au citoyen.")
        return redirect('admin_demandes')
    return render(request, 'demandes/admin/traitement-demande.html', {
        'demande': demande,
        'statuts': Demande.STATUT_CHOICES,
    })
