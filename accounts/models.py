from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('citoyen', 'Citoyen'),
        ('agent', 'Agent Administratif'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citoyen')
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_citoyen(self):
        return self.role == 'citoyen'

    @property
    def is_agent(self):
        return self.role == 'agent'

    @property
    def is_admin_servicepub(self):
        return self.role == 'admin'


class Citoyen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_citoyen')
    CINE = models.CharField(max_length=20, unique=True, verbose_name='Numéro CINE')
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to='citoyens/photos/', blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Citoyen'
        verbose_name_plural = 'Citoyens'

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.CINE}"


class AgentAdministratif(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_agent')
    administration = models.CharField(max_length=250, verbose_name="Administration")
    code_acces = models.CharField(max_length=50, unique=True, verbose_name="Code d'accès")
    poste = models.CharField(max_length=150, blank=True)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Agent Administratif'
        verbose_name_plural = 'Agents Administratifs'

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.administration}"
