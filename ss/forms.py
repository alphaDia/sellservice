from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, AnnonceModel
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', "password1", "password2")
        labels = {
            "password1": _("Mot de passe"),
            "password2": _("Confirmation")
        }


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for field in self.fields.keys():
            self.fields[field].required = False

            if 'password1' == field:
                self.fields[field].label = _('Mot de passe')

            if 'password2' == field:
                self.fields[field].label = _('Confirmation')

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'aria-label': 'email'}),
            'first_name': forms.TextInput(attrs={'aria-label': 'nom'}),
            'last_name': forms.TextInput(attrs={'aria-label': 'prenom'}),
        }

        error_messages = {
            'email': {
                'invalid': 'utilisateur existe deja',
            }
        }


class LoginUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password1')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'password_lost'}),
            # 'email': forms.EmailInput(attrs={'placeholder': 'Email'})
        }


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False

    class Meta:
        model = User
        fields = ['profile_image', 'first_name', 'last_name',
                  'biographie', 'tel_number', ]


class AnnonceForm(forms.ModelForm):
    class Meta:
        model = AnnonceModel
        fields = ['categorie', 'title', 'description', 'annonce_image']
