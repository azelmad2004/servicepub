from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    InscriptionCitoyenForm, InscriptionAdminForm,
    ConnexionCitoyenForm, ConnexionAdminForm,
    ProfilCitoyenForm, MotDePasseOublieForm
)


def inscription_citoyen(request):
    if request.method == 'POST':
        form = InscriptionCitoyenForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Votre compte a été créé.")
            return redirect('citoyen_dashboard')
    else:
        form = InscriptionCitoyenForm()
    return render(request, 'accounts/S_inscrire.html', {'form': form, 'active_tab': 'citoyen'})


def inscription_admin(request):
    if request.method == 'POST':
        form = InscriptionAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Votre demande d'accès est en cours de validation (48h).")
            return redirect('connexion_admin')
    else:
        form = InscriptionAdminForm()
    return render(request, 'accounts/S_inscrire.html', {'form': form, 'active_tab': 'administration'})


def connexion_citoyen(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profil_citoyen'):
            return redirect('citoyen_dashboard')
        return redirect('admin_dashboard')
    if request.method == 'POST':
        form = ConnexionCitoyenForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            messages.success(request, f"Bonjour {user.first_name} !")
            next_url = request.GET.get('next', 'citoyen_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = ConnexionCitoyenForm()
    return render(request, 'accounts/se_connecter.html', {'form': form, 'active_tab': 'citoyen'})


def connexion_admin(request):
    if request.method == 'POST':
        form = ConnexionAdminForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role in ['agent', 'admin']:
                login(request, user)
                messages.success(request, f"Bienvenue {user.first_name} !")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Accès refusé. Compte agent requis.")
        else:
            messages.error(request, "Identifiants incorrects.")
    else:
        form = ConnexionAdminForm()
    return render(request, 'accounts/se_connecter.html', {'form': form, 'active_tab': 'administration'})


def deconnexion(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('index')


def mot_de_passe_oublie(request):
    if request.method == 'POST':
        form = MotDePasseOublieForm(request.POST)
        if form.is_valid():
            messages.info(request, "Un email de réinitialisation a été envoyé.")
    else:
        form = MotDePasseOublieForm()
    return render(request, 'accounts/mot-de-passe-oublie.html', {'form': form})


@login_required
def profil_citoyen(request):
    try:
        citoyen = request.user.profil_citoyen
    except Exception:
        messages.error(request, "Profil citoyen introuvable.")
        return redirect('index')
    if request.method == 'POST':
        form = ProfilCitoyenForm(request.POST, request.FILES, instance=citoyen)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profil_citoyen')
    else:
        form = ProfilCitoyenForm(instance=citoyen)
    return render(request, 'accounts/profil-citoyen.html', {'form': form, 'citoyen': citoyen})
