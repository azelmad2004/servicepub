from django import forms
from .models import Demande, Document


class NouvelleDemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['notes_citoyen', 'adresse_livraison']
        widgets = {
            'notes_citoyen': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Informations complémentaires...'}),
            'adresse_livraison': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Adresse de livraison du document'}),
        }
        labels = {
            'notes_citoyen': 'Informations complémentaires',
            'adresse_livraison': 'Adresse de livraison',
        }


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['titre', 'fichier']
        widgets = {
            'fichier': forms.ClearableFileInput(attrs={'accept': '.pdf'}),
        }
        labels = {
            'titre': 'Nom du document',
            'fichier': 'Fichier (PDF uniquement)',
        }

    def clean_fichier(self):
        fichier = self.cleaned_data.get('fichier', False)
        if fichier:
            if not fichier.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Veuillez télécharger un fichier PDF valide.')
        return fichier
