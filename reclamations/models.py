from django.db import models
import uuid
from accounts.models import Citoyen, User


def generate_ticket():
    return 'TK-' + str(uuid.uuid4()).upper()[:6]


class Reclamation(models.Model):
    CATEGORIE_CHOICES = [
        ('retard', 'Retard de traitement'),
        ('erreur_doc', 'Erreur dans le document'),
        ('mauvais_service', 'Mauvais service'),
        ('paiement', 'Problème de paiement'),
        ('autre', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('ouverte', 'Ouverte'),
        ('en_cours', 'En cours de traitement'),
        ('resolue', 'Résolue'),
        ('fermee', 'Fermée'),
    ]
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='reclamations')
    sujet = models.CharField(max_length=300)
    categorie = models.CharField(max_length=30, choices=CATEGORIE_CHOICES)
    description = models.TextField()
    numero_ticket = models.CharField(max_length=20, unique=True, default=generate_ticket)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ouverte')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    piece_jointe = models.FileField(upload_to='reclamations/', blank=True, null=True)

    class Meta:
        verbose_name = 'Réclamation'
        verbose_name_plural = 'Réclamations'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.numero_ticket} — {self.sujet[:50]}"


class Message(models.Model):
    reclamation = models.ForeignKey(Reclamation, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    piece_jointe = models.FileField(upload_to='messages/', blank=True, null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['date_envoi']

    def __str__(self):
        return f"Message de {self.auteur.get_full_name()} — {self.reclamation.numero_ticket}"
