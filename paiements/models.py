from django.db import models
from demandes.models import Demande


class Paiement(models.Model):
    METHODE_CHOICES = [
        ('carte', 'Carte bancaire'),
        ('virement', 'Virement bancaire'),
        ('especes', 'Espèces'),
        ('cmi', 'CMI (Centre Monétique)'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('echoue', 'Échoué'),
        ('rembourse', 'Remboursé'),
    ]
    demande = models.OneToOneField(Demande, on_delete=models.CASCADE, related_name='paiement')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode = models.CharField(max_length=20, choices=METHODE_CHOICES, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    transaction_id = models.CharField(max_length=100, blank=True)
    date_paiement = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    recu = models.FileField(upload_to='reçus/', blank=True, null=True)

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        return f"Paiement {self.demande.reference} — {self.montant} MAD ({self.get_statut_display()})"
