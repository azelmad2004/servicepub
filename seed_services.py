import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicepub.settings')
django.setup()

from services.models import ServiceAdministratif

services = [
    {
        'nom': "Acte de Naissance (Copie intégrale)",
        'description': "Demande d'une copie intégrale de l'acte de naissance original.",
        'categorie': 'etat_civil',
        'tarif': 20.00,
        'delai_jours': 3,
        'documents_requis': "Copie du livret de famille ou ancienne copie d'acte de naissance."
    },
    {
        'nom': "Extrait d'Acte de Naissance",
        'description': "Document prouvant l'identité et la filiation d'un individu.",
        'categorie': 'etat_civil',
        'tarif': 10.00,
        'delai_jours': 2,
        'documents_requis': "Copie du livret de famille."
    },
    {
        'nom': "Attestation de Résidence",
        'description': "Document certifiant le domicile actuel du citoyen.",
        'categorie': 'residence',
        'tarif': 50.00,
        'delai_jours': 5,
        'documents_requis': "Contrat de bail ou facture (Eau/Électricité) de moins de 3 mois."
    },
    {
        'nom': "Légalisation de Signature",
        'description': "Certification de l'authenticité d'une signature sur un document.",
        'categorie': 'legalisation',
        'tarif': 5.00,
        'delai_jours': 1,
        'documents_requis': "Document original non signé + CIN originale."
    },
    {
        'nom': "Copie Certifiée Conforme",
        'description': "Certification qu'une copie est identique à l'original.",
        'categorie': 'legalisation',
        'tarif': 2.00,
        'delai_jours': 1,
        'documents_requis': "Document original + photocopie."
    }
]

for s_data in services:
    ServiceAdministratif.objects.get_or_create(nom=s_data['nom'], defaults=s_data)

print(f"Successfully created {len(services)} services.")
