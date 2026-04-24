from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Citoyen
from services.models import ServiceAdministratif
from demandes.models import Demande
from paiements.models import Paiement

User = get_user_model()

class PaiementsTestCase(TestCase):
    def setUp(self):
        self.citoyen_user = User.objects.create_user(
            username='citoyen@test.com', email='citoyen@test.com', password='password123', role='citoyen'
        )
        self.citoyen_profil = Citoyen.objects.create(
            user=self.citoyen_user, CINE='AB123456'
        )
        self.service = ServiceAdministratif.objects.create(
            nom="Acte", description="Test", categorie="etat_civil", tarif=20.00, delai_jours=5
        )
        self.demande = Demande.objects.create(
            reference='REF123', citoyen=self.citoyen_profil, service=self.service, statut='en_cours'
        )
        self.paiement_obj = Paiement.objects.create(
            demande=self.demande, montant=20.00
        )

    def test_paiement_process(self):
        self.client.login(username='citoyen@test.com', password='password123')
        response = self.client.post(reverse('paiement', args=[self.demande.id]), {
            'methode': 'carte'
        })
        self.paiement_obj.refresh_from_db()
        self.assertEqual(self.paiement_obj.statut, 'paye')
        self.assertEqual(self.paiement_obj.methode, 'carte')
        self.assertIsNotNone(self.paiement_obj.transaction_id)
        self.demande.refresh_from_db()
        self.assertEqual(self.demande.statut, 'en_traitement')
        self.assertRedirects(response, reverse('detail_demande', args=[self.demande.id]))
