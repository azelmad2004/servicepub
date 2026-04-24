from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reclamation, Message
from .forms import ReclamationForm, MessageForm


@login_required
def liste_reclamations_citoyen(request):
    if not hasattr(request.user, 'profil_citoyen'):
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    citoyen = request.user.profil_citoyen
    reclamations = Reclamation.objects.filter(citoyen=citoyen).order_by('-date_creation')
    return render(request, 'reclamations/reclamations-citoyen.html', {
        'reclamations': reclamations,
        'reclamation_form': ReclamationForm(),
    })


@login_required
def nouvelle_reclamation(request):
    if not hasattr(request.user, 'profil_citoyen'):
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    citoyen = request.user.profil_citoyen
    if request.method == 'POST':
        form = ReclamationForm(request.POST, request.FILES)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.citoyen = citoyen
            rec.save()
            messages.success(request, f"Réclamation {rec.numero_ticket} soumise avec succès.")
            return redirect('liste_reclamations_citoyen')
    else:
        form = ReclamationForm()
    return render(request, 'reclamations/reclamations-citoyen.html', {
        'reclamations': Reclamation.objects.filter(citoyen=citoyen).order_by('-date_creation'),
        'reclamation_form': form,
        'show_modal': True,
    })


@login_required
def detail_reclamation(request, rec_id):
    if not hasattr(request.user, 'profil_citoyen'):
        messages.error(request, "Accès réservé aux citoyens.")
        return redirect('index')
    citoyen = request.user.profil_citoyen
    reclamation = get_object_or_404(Reclamation, id=rec_id, citoyen=citoyen)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.reclamation = reclamation
            msg.auteur = request.user
            msg.save()
            return redirect('detail_reclamation', rec_id=reclamation.id)
    else:
        form = MessageForm()
    messages_list = reclamation.messages.all()
    return render(request, 'reclamations/reclamations-citoyen.html', {
        'reclamation': reclamation,
        'messages_list': messages_list,
        'message_form': form,
        'reclamation_form': ReclamationForm(),
        'reclamations': Reclamation.objects.filter(citoyen=citoyen),
    })


@login_required
def admin_reclamations(request):
    if request.user.role not in ['agent', 'admin']:
        return redirect('index')
    statut_filtre = request.GET.get('statut', '')
    reclamations = Reclamation.objects.all().select_related('citoyen__user')
    if statut_filtre:
        reclamations = reclamations.filter(statut=statut_filtre)
    return render(request, 'reclamations/reclamations-admin.html', {
        'reclamations': reclamations,
        'statuts': Reclamation.STATUT_CHOICES,
        'statut_filtre': statut_filtre,
    })


@login_required
def admin_repondre_reclamation(request, rec_id):
    if request.user.role not in ['agent', 'admin']:
        return redirect('index')
    reclamation = get_object_or_404(Reclamation, id=rec_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.reclamation = reclamation
            msg.auteur = request.user
            msg.save()
            nouveau_statut = request.POST.get('statut')
            if nouveau_statut:
                reclamation.statut = nouveau_statut
                reclamation.save()
            messages.success(request, "Réponse envoyée.")
            return redirect('admin_reclamations')
    else:
        form = MessageForm()
    
    messages_list = reclamation.messages.all()
    return render(request, 'reclamations/reclamations-admin.html', {
        'reclamation': reclamation,
        'messages_list': messages_list,
        'message_form': form,
        'statuts': Reclamation.STATUT_CHOICES,
        'reclamations': Reclamation.objects.all(),
    })
