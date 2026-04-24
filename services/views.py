from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceAdministratif
from accounts.models import AgentAdministratif, Citoyen


def liste_services(request):
    services = ServiceAdministratif.objects.filter(actif=True).order_by('categorie', 'nom')
    return render(request, 'services/liste.html', {'services': services})


@login_required
def admin_gestion_services(request):
    if request.user.role not in ['agent', 'admin']:
        return redirect('index')
    services = ServiceAdministratif.objects.all().order_by('categorie', 'nom')
    return render(request, 'services/admin_gestion.html', {'services': services})


@login_required
def admin_toggle_service(request, service_id):
    if request.user.role != 'admin':
        return redirect('index')
    service = get_object_or_404(ServiceAdministratif, id=service_id)
    service.actif = not service.actif
    service.save()
    messages.success(request, f"Service '{service.nom}' {'activé' if service.actif else 'désactivé'}.")
    return redirect('admin_gestion_services')


@login_required
def admin_gestion_agents(request):
    if request.user.role != 'admin':
        return redirect('index')
    agents = AgentAdministratif.objects.select_related('user').all()
    return render(request, 'services/admin_agents.html', {'agents': agents})


@login_required
def admin_gestion_citoyens(request):
    if request.user.role not in ['agent', 'admin']:
        return redirect('index')
    q = request.GET.get('q', '')
    citoyens = Citoyen.objects.select_related('user').all()
    if q:
        citoyens = citoyens.filter(
            user__first_name__icontains=q
        ) | citoyens.filter(
            user__last_name__icontains=q
        ) | citoyens.filter(CINE__icontains=q)
    return render(request, 'services/admin_citoyens.html', {
        'citoyens': citoyens, 'q': q,
        'total': Citoyen.objects.count(),
    })
