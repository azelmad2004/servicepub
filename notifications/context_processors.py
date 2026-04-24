from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(destinataire=request.user, lue=False).count()
        return {'notifications_count': count}
    return {'notifications_count': 0}
