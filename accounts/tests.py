from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Citoyen, AgentAdministratif

User = get_user_model()

class AccountsTestCase(TestCase):
    def setUp(self):
        self.citoyen_user = User.objects.create_user(
            username='citoyen@test.com',
            email='citoyen@test.com',
            password='password123',
            role='citoyen',
            first_name='Jean',
            last_name='Dupont'
        )
        self.citoyen_profil = Citoyen.objects.create(
            user=self.citoyen_user, CINE='AB123456'
        )
        self.agent_user = User.objects.create_user(
            username='agent@test.com',
            email='agent@test.com',
            password='password123',
            role='agent',
            first_name='Admin',
            last_name='Agent'
        )
        self.agent_profil = AgentAdministratif.objects.create(
            user=self.agent_user, administration='Mairie', code_acces='AG123'
        )

    def test_connexion_citoyen(self):
        response = self.client.post(reverse('connexion_citoyen'), {
            'username': 'citoyen@test.com',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('citoyen_dashboard'))

    def test_connexion_admin(self):
        response = self.client.post(reverse('connexion_admin'), {
            'username': 'agent@test.com',
            'password': 'password123',
            'code_acces': 'AG123'
        })
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_access_denied_for_agent_on_citoyen_view(self):
        self.client.login(username='agent@test.com', password='password123')
        response = self.client.get(reverse('citoyen_dashboard'))
        self.assertRedirects(response, reverse('admin_dashboard'))
