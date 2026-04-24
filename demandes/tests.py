from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from services.models import ServiceAdministratif
from accounts.models import Citoyen, AgentAdministratif
from demandes.models import Demande

User = get_user_model()

class DemandesTestCase(TestCase):
    def setUp(self):
        self.citoyen_user = User.objects.create_user(
            username='citoyen@test.com', email='citoyen@test.com', password='password123', role='citoyen'
        )
        self.citoyen_profil = Citoyen.objects.create(
            user=self.citoyen_user, CINE='AB123456'
        )
        self.agent_user = User.objects.create_user(
            username='agent@test.com', email='agent@test.com', password='password123', role='agent'
        )
        self.agent_profil = AgentAdministratif.objects.create(
            user=self.agent_user, administration='Mairie', code_acces='AG123'
        )
        self.service = ServiceAdministratif.objects.create(
            nom="Acte de naissance", description="Test", categorie="etat_civil", tarif=20.00, delai_jours=5
        )

    def test_creation_demande_citoyen(self):
        self.client.login(username='citoyen@test.com', password='password123')
        response = self.client.post(reverse('choisir_service', args=[self.service.id]), {
            'reference': 'REF123',
            'notes': 'Test de note'
        })
        self.assertEqual(Demande.objects.count(), 1)
        demande = Demande.objects.first()
        self.assertEqual(demande.citoyen, self.citoyen_profil)
        self.assertEqual(demande.service, self.service)
        self.assertRedirects(response, reverse('upload_documents', args=[demande.id]))

    def test_agent_can_see_demandes(self):
        Demande.objects.create(
            reference='REF456', citoyen=self.citoyen_profil, service=self.service, statut='en_cours'
        )
        self.client.login(username='agent@test.com', password='password123')
        response = self.client.get(reverse('admin_demandes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'REF456')

    def test_citoyen_cannot_see_admin_demandes(self):
        self.client.login(username='citoyen@test.com', password='password123')
        response = self.client.get(reverse('admin_demandes'))
        self.assertRedirects(response, reverse('index'))
