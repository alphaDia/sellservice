from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext as _
from . import managers
# Create your models here.
from django.utils import timezone


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(_('Adress mail'), unique=True)
    first_name = models.CharField(_('Nom'), max_length=100, default="")
    last_name = models.CharField(_('Prenom'), max_length=100, default="")
    password1 = models.CharField(_('Password'), max_length=255, default="")
    description = models.TextField(
        _('Bio'), help_text="faite une description de vous",  max_length=400, default=" ")
    tel_number = models.CharField(
        _("Numero Tel"), help_text="Numero: (224)", default=" ", max_length=15)
    avatar = models.ImageField(_('image'), default="")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    promotteur = models.BooleanField(default=False)

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


class Annonce(models.Model):
    service = models.CharField(
        max_length=200, null=False, blank=False, help_text="the publish service type")

    categorie = models.CharField(max_length=300, blank=False, null=False,
                                 help_text="possible categorie of the publish service")

    titre = models.CharField(max_length=100, blank=False, null=False,
                             help_text="Mettez un titre accrocheur sur votre annonce")

    parcours = models.TextField(max_length=400, blank=False, null=False,
                                help_text="Decrivez votre parcours")

    publish_date = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre


class Notification(models.Model):
    notif_content = models.TextField(max_length=300, blank=False, null=False)
    simple_user = models.ManyToManyField(
        User, through="User_Notification")
    isRead = models.BooleanField(default=False)


class User_Notification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="notif date", auto_now_add=True)

    def __str__(self):
        return f'{self.notification.notif_content} {self.user.email}'
