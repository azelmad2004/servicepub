from django import forms
from .models import Reclamation, Message


class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['sujet', 'categorie', 'description', 'piece_jointe']
        widgets = {
            'sujet': forms.TextInput(attrs={
                'placeholder': "Titre de votre réclamation",
                'style': "width: 100%; padding: 12px; border: 1px solid #e2e8f0; border-radius: 8px;"
            }),
            'categorie': forms.Select(attrs={
                'style': "width: 100%; padding: 12px; border: 1px solid #e2e8f0; border-radius: 8px;"
            }),
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': "Décrivez votre problème...",
                'style': "width: 100%; padding: 12px; border: 1px solid #e2e8f0; border-radius: 8px; resize: none;"
            }),
        }
        labels = {
            'sujet': 'Sujet',
            'categorie': 'Catégorie',
            'description': 'Description',
            'piece_jointe': 'Pièce jointe (optionnel)',
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contenu', 'piece_jointe']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': "Votre message...",
                'style': "width: 100%; padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px; resize: none;"
            }),
        }
        labels = {
            'contenu': 'Message',
            'piece_jointe': 'Pièce jointe (optionnel)',
        }
