from django.db import models
from accounts.models import User


class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('succes', 'Succès'),
        ('alerte', 'Alerte'),
        ('urgent', 'Urgent'),
    ]
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    type_notif = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    lue = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)
    lien = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-date_envoi']

    def __str__(self):
        return f"[{self.get_type_notif_display()}] {self.titre} → {self.destinataire.get_full_name()}"
