from django import forms
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.text import slugify
from .models import User, Citoyen, AgentAdministratif


class InscriptionCitoyenForm(UserCreationForm):
    prenom = forms.CharField(max_length=100, label="Prénom")
    nom = forms.CharField(max_length=100, label="Nom")
    email = forms.EmailField(label="Email")
    telephone = forms.CharField(max_length=20, label="Téléphone")
    CINE = forms.CharField(max_length=20, label="Numéro CINE")
    date_naissance = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    lieu_naissance = forms.CharField(max_length=150, label="Lieu de naissance")
    adresse = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), label="Adresse")
    accepter_cgu = forms.BooleanField(label="J'accepte les CGU", required=True)

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'telephone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['prenom'].widget.attrs.update({'placeholder': 'Votre prénom'})
        self.fields['nom'].widget.attrs.update({'placeholder': 'Votre nom'})
        self.fields['email'].widget.attrs.update({'placeholder': 'votre@email.com'})
        self.fields['telephone'].widget.attrs.update({'placeholder': '06XXXXXXXX'})
        self.fields['CINE'].widget.attrs.update({'placeholder': 'Ex: AB123456'})
        self.fields['lieu_naissance'].widget.attrs.update({'placeholder': 'Ex: Casablanca'})
        self.fields['adresse'].widget.attrs.update({'placeholder': 'Votre adresse complète', 'rows': '2'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Minimum 8 caractères'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmez le mot de passe'})
        self.fields['accepter_cgu'].widget.attrs.update({'class': ''}) # Checkbox shouldn't have form-control usually

    def clean_CINE(self):
        cine = self.cleaned_data.get('CINE')
        if Citoyen.objects.filter(CINE=cine).exists():
            raise forms.ValidationError("Un compte avec ce numéro CINE existe déjà.")
        return cine

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà. Veuillez vous connecter.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['prenom']
        user.last_name = self.cleaned_data['nom']
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.telephone = self.cleaned_data['telephone']
        user.adresse = self.cleaned_data['adresse']
        user.role = 'citoyen'
        if commit:
            user.save()
            Citoyen.objects.create(
                user=user,
                CINE=self.cleaned_data['CINE'],
                date_naissance=self.cleaned_data['date_naissance'],
                lieu_naissance=self.cleaned_data['lieu_naissance'],
            )
        return user


class InscriptionAdminForm(UserCreationForm):
    prenom = forms.CharField(max_length=100, label="Prénom")
    nom = forms.CharField(max_length=100, label="Nom")
    email = forms.EmailField(label="Email professionnel")
    telephone = forms.CharField(max_length=20, label="Téléphone")
    administration = forms.CharField(max_length=250, label="Nom de l'administration")
    code_agrement = forms.CharField(max_length=50, label="Code d'agrément")
    poste = forms.CharField(max_length=150, label="Poste / Fonction")

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'telephone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['prenom'].widget.attrs.update({'placeholder': 'Votre prénom'})
        self.fields['nom'].widget.attrs.update({'placeholder': 'Votre nom'})
        self.fields['email'].widget.attrs.update({'placeholder': 'votre@email.prof'})
        self.fields['telephone'].widget.attrs.update({'placeholder': '06XXXXXXXX'})
        self.fields['administration'].widget.attrs.update({'placeholder': 'Ex: Ministère de l\'Intérieur'})
        self.fields['code_agrement'].widget.attrs.update({'placeholder': 'Code fourni par votre administration'})
        self.fields['poste'].widget.attrs.update({'placeholder': 'Ex: Chef de service'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mot de passe sécurisé'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmez'})

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà. Veuillez vous connecter.")
        return email

    def clean_code_agrement(self):
        code = self.cleaned_data.get('code_agrement')
        if AgentAdministratif.objects.filter(code_acces=code).exists():
            raise forms.ValidationError("Ce code d'agrément est déjà utilisé par un autre agent.")
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['prenom']
        user.last_name = self.cleaned_data['nom']
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.telephone = self.cleaned_data['telephone']
        user.role = 'agent'
        user.is_active = True  # FAST CONNECTION for testing (keep 48h labels for realism)
        if commit:
            user.save()
            AgentAdministratif.objects.create(
                user=user,
                administration=self.cleaned_data['administration'],
                code_acces=self.cleaned_data['code_agrement'],
                poste=self.cleaned_data['poste'],
            )
        return user


class ConnexionCitoyenForm(AuthenticationForm):
    username = forms.EmailField(label="Adresse email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Votre mot de passe'}))
    remember_me = forms.BooleanField(required=False, label="Se souvenir de moi")

    def clean(self):
        cleaned_data = super().clean()
        user = self.user_cache
        if user and user.role != 'citoyen':
            raise forms.ValidationError("Cet espace est réservé aux citoyens. Veuillez utiliser l'espace Administration.")
        return cleaned_data


class ConnexionAdminForm(AuthenticationForm):
    username = forms.EmailField(label="Email professionnel", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.prof'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Votre mot de passe'}))
    code_acces = forms.CharField(max_length=50, label="Code d'accès sécurisé", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Code d'accès"}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        code_acces = self.cleaned_data.get('code_acces')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            
            # Check for inactive account
            if self.user_cache is None:
                # See if user exists but is inactive
                user_obj = User.objects.filter(username=username).first()
                if user_obj and not user_obj.is_active:
                    raise forms.ValidationError("Votre compte est en attente de validation par l'administration (48h).")
                raise forms.ValidationError("Email ou mot de passe incorrect.")
            
            user = self.user_cache
            if user.role not in ['agent', 'admin']:
                raise forms.ValidationError("Cet espace est réservé au personnel administratif.")
            
            try:
                agent = user.profil_agent
                if agent.code_acces != code_acces:
                     raise forms.ValidationError("Le code d'accès sécurisé est incorrect.")
            except AgentAdministratif.DoesNotExist:
                if user.role == 'agent':
                    raise forms.ValidationError("Profil administratif introuvable.")
        
        return self.cleaned_data


class ProfilCitoyenForm(forms.ModelForm):
    class Meta:
        model = Citoyen
        fields = ['date_naissance', 'lieu_naissance', 'photo']
        widgets = {'date_naissance': forms.DateInput(attrs={'type': 'date'})}


class MotDePasseOublieForm(forms.Form):
    email = forms.EmailField(label="Votre adresse email")
