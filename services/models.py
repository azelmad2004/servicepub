from django.db import models


class ServiceAdministratif(models.Model):
    CATEGORIE_CHOICES = [
        ('etat_civil', 'État Civil'),
        ('identite', "Documents d'identité"),
        ('transport', 'Transports'),
        ('autre', 'Autre'),
    ]
    nom = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    tarif = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delai_jours = models.IntegerField(default=5, verbose_name="Délai (jours)")
    conditions = models.TextField(blank=True, verbose_name="Conditions d'accès")
    documents_requis = models.TextField(blank=True, verbose_name="Documents requis")
    actif = models.BooleanField(default=True)
    icone = models.CharField(max_length=100, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Service Administratif'
        verbose_name_plural = 'Services Administratifs'
        ordering = ['categorie', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.get_categorie_display()})"
