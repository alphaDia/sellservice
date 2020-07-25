from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Annonce
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name',)
        widgets = {
            'email': forms.EmailInput(attrs={'aria-label': 'email'}),
            'first_name': forms.TextInput(attrs={'aria-label': 'nom'}),
            'last_name': forms.TextInput(attrs={'aria-label': 'prenom'}),
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
        fields = ['first_name', 'last_name',
                  'description', 'tel_number', ]

    def clean_tel_number(self):
        import re

        tel_number = self.cleaned_data.get('tel_number')
        if not re.match(r"(|^\00|\+\d{3}\d{9}$)", tel_number, re.M):
            raise ValidationError(
                _("Sil vous plait entrer un numero correcte"))

        """if not re.match(r'', tel_number):
            raise ValidationError(_("Ce numero est incorrecte"))"""

    def clean_description(self):
        pass


class dropeAnnounceForm(forms.Form):
    pass
