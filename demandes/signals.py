from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Demande
from notifications.models import Notification

@receiver(post_save, sender=Demande)
def notification_nouvelle_demande(sender, instance, created, **kwargs):
    if created:
        # Notifier le citoyen
        Notification.objects.create(
            destinataire=instance.citoyen.user,
            titre="Demande enregistrée",
            contenu=f"Votre demande pour le service '{instance.service.nom}' a été reçue avec succès. Elle est actuellement en cours de traitement.",
            type_notif='succes',
            lien=f"/demandes/{instance.id}/"
        )
        
        # On pourrait aussi simuler une réponse automatique de l'admin
        # mais une notification est plus standard pour une "réponse automatique" initiale.
