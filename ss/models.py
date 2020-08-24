from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext as _
from . import managers
# Create your models here.
from django.utils import timezone


def user_directory_path(user, filename):
    return "images/user_{0}/{1}".format(user.id, filename)


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(_('Adress mail'), unique=True)
    first_name = models.CharField(_('Nom'), max_length=100, default="")
    last_name = models.CharField(_('Prenom'), max_length=100, default="")
    password1 = models.CharField(_('Password'), max_length=255, default="")
    biographie = models.TextField(
        _('Bio'), help_text="faite une description de vous",  max_length=400, default=" ")
    tel_number = models.CharField(
        _("Numero Tel"), help_text="Numero: (224)", default="", max_length=15)
    profile_image = models.ImageField(
        _("Image du profil"), upload_to=user_directory_path, default="")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.UserManger()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        from django.shortcuts import reverse
        return reverse('profile', kwargs={'id': self.id})


class Categories(models.Model):
    categorie_name = models.CharField(
        _('Nom de la categorie'), max_length=100,
        blank=False, null=False, help_text="Nom de la categorie")
    service = models.ForeignKey(
        'Service', on_delete=models.CASCADE,)

    def __str__(self):
        return self.categorie_name


class Service(models.Model):
    service_type = models.CharField(
        _('Type du service'), max_length=100,
        blank=False, null=False, help_text="type du service ex: informatique")

    def __str__(self):
        return self.service_type


def user_directory_path2(instance, filename):
    return "annonce/images/user_{0}/{1}".format(instance.user.id, filename)


class AnnonceModel(models.Model):
    categorie = models.CharField(max_length=100, blank=False, null=False)

    title = models.CharField(_('titre'), max_length=100, blank=False, null=False,
                             help_text="Donnez un titre a votre annonce", default="")

    description = models.TextField(max_length=400, blank=False, null=False,
                                   help_text="Decrivez votre annonce", default="")

    publish_date = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    annonce_image = models.ImageField(
        upload_to=user_directory_path2, default="")

    def get_absolute_url(self):
        return reverse('annonce-detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title


class Interet(models.Model):
    annonce = models.ForeignKey(AnnonceModel, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Notification(models.Model):
    notif_content = models.TextField(max_length=300, blank=False, null=False)
    interet = models.ForeignKey(Interet, on_delete=models.CASCADE)
    isRead = models.BooleanField(default=False)
