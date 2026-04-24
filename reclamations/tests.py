from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Citoyen, AgentAdministratif
from reclamations.models import Reclamation, Message

User = get_user_model()

class ReclamationsTestCase(TestCase):
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

    def test_creation_reclamation(self):
        self.client.login(username='citoyen@test.com', password='password123')
        response = self.client.post(reverse('nouvelle_reclamation'), {
            'sujet': 'Problème de paiement',
            'categorie': 'paiement',
            'description': 'Le paiement a échoué'
        })
        self.assertEqual(Reclamation.objects.count(), 1)
        rec = Reclamation.objects.first()
        self.assertEqual(rec.citoyen, self.citoyen_profil)
        self.assertRedirects(response, reverse('liste_reclamations_citoyen'))

    def test_reponse_reclamation_agent(self):
        rec = Reclamation.objects.create(
            citoyen=self.citoyen_profil, sujet='Test', categorie='autre', numero_ticket='TICKET-002'
        )
        self.client.login(username='agent@test.com', password='password123')
        response = self.client.post(reverse('admin_repondre_reclamation', args=[rec.id]), {
            'contenu': 'Nous traitons votre demande.',
            'statut': 'en_cours'
        })
        self.assertEqual(Message.objects.count(), 1)
        rec.refresh_from_db()
        self.assertEqual(rec.statut, 'en_cours')
        self.assertRedirects(response, reverse('admin_reclamations'))
