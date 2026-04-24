from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification


@login_required
def liste_notifications(request):
    filtre = request.GET.get('filter', 'all')
    notifications = Notification.objects.filter(destinataire=request.user).order_by('-date_envoi')
    
    if filtre == 'unread':
        notifications = notifications.filter(lue=False)
    elif filtre == 'read':
        notifications = notifications.filter(lue=True)
        
    non_lues = Notification.objects.filter(destinataire=request.user, lue=False).count()
    return render(request, 'notifications/notifications-citoyen.html', {
        'notifications': notifications,
        'non_lues': non_lues,
    })


@login_required
def marquer_lue(request, notif_id):
    Notification.objects.filter(id=notif_id, destinataire=request.user).update(lue=True)
    return redirect(request.META.get('HTTP_REFERER', 'liste_notifications'))


@login_required
def marquer_toutes_lues(request):
    Notification.objects.filter(destinataire=request.user, lue=False).update(lue=True)
    return redirect('liste_notifications')


@login_required
def count_non_lues(request):
    count = Notification.objects.filter(destinataire=request.user, lue=False).count()
    return JsonResponse({'count': count})
