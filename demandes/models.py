from django.db import models
import uuid
from accounts.models import Citoyen, AgentAdministratif
from services.models import ServiceAdministratif


def generate_reference():
    return 'SP-' + str(uuid.uuid4()).upper()[:8]


class Demande(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('en_attente_docs', 'En attente de documents'),
        ('en_traitement', 'En traitement'),
        ('traitee', 'Traitée'),
        ('rejetee', 'Rejetée'),
        ('livree', 'Livrée'),
    ]
    reference = models.CharField(max_length=30, unique=True, default=generate_reference)
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='demandes')
    service = models.ForeignKey(ServiceAdministratif, on_delete=models.PROTECT, related_name='demandes')
    agent = models.ForeignKey(
        AgentAdministratif, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='demandes_assignees'
    )
    statut = models.CharField(max_length=30, choices=STATUT_CHOICES, default='en_cours')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_echeance = models.DateField(null=True, blank=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    notes_citoyen = models.TextField(blank=True)
    notes_agent = models.TextField(blank=True)
    adresse_livraison = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Demande'
        verbose_name_plural = 'Demandes'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.reference} — {self.service.nom} ({self.get_statut_display()})"

    def get_statut_badge(self):
        badges = {
            'en_cours': 'warning',
            'en_attente_docs': 'info',
            'en_traitement': 'primary',
            'traitee': 'success',
            'rejetee': 'danger',
            'livree': 'success',
        }
        return badges.get(self.statut, 'secondary')


class Document(models.Model):
    TYPE_CHOICES = [
        ('justificatif', 'Document justificatif'),
        ('officiel', 'Document officiel généré'),
        ('autre', 'Autre'),
    ]
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=200)
    type_doc = models.CharField(max_length=30, choices=TYPE_CHOICES, default='justificatif')
    fichier = models.FileField(upload_to='documents/%Y/%m/')
    description = models.TextField(blank=True)
    date_upload = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"{self.titre} ({self.demande.reference})"
