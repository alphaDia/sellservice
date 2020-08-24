from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import login,  authenticate, logout
from django.template.context_processors import csrf
from django.http import HttpResponse
from crispy_forms.utils import render_crispy_form
from .models import User
from django.views.generic import DetailView
from django.contrib import messages
import json
from . import forms
from .models import Service, Categories, AnnonceModel, AnnonceModel
# Create your views here.


def form_render(form, request):
    ctx = {}
    ctx.update(csrf(request))
    return render_crispy_form(form, context=ctx)


def log_out(request):

    logout(request)
    messages.info(
        request, "Nous esperons vous revoire bientot sur notre plateforme")

    return redirect('index')


class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = forms.LoginUserForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginUserForm(data=request.POST)

        username = request.POST['email']
        raw_password = request.POST['password1']
        user = authenticate(username=username, password=raw_password)

        if user is not None:
            login(request, user)
            messages.info(
                request, f"Bienvenu {request.user.first_name} {request.user.last_name}")

            return HttpResponse(json.dumps({'success': True, 'redirect_url': '/'}), content_type='application/json')

        loginForm = form_render(form, request)

        return HttpResponse(json.dumps({'success': False, 'form_html': loginForm}), content_type='application/json')


class Index(View):
    template_name = 'ss/index.html'

    def getAll(self):

        ctx = {
            'services': Service.objects.all(),
            'designGraphismes': Categories.objects.filter(service__service_type__iexact="Design & Graphisme"),
            'redactions': Categories.objects.filter(service__service_type__iexact="Redaction"),
            'audiovisuels': Categories.objects.filter(service__service_type__iexact="Audiovisuel"),
            'siteDeveloppements': Categories.objects.filter(service__service_type__iexact="Site & Développement"),
            'formationCoachings': Categories.objects.filter(service__service_type__iexact="Formations & Coaching")
        }

        return ctx

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.getAll())


class SignUp(View):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = forms.SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = forms.SignupForm(data=request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)

            if user is not None:
                login(request, user)
                messages.success(request, "Votre Compte est cree avec success")

            return HttpResponse(json.dumps({'success': True, 'redirect_url': '/', }), content_type='application/json')

        signupForm = form_render(form, request)

        return HttpResponse(json.dumps({'success': False, 'form_html': signupForm}), content_type='application/json')


class Annonce(View):
    template_name = "ss/annonce.html"

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:

            messages.info(
                request, "Vous devez avoir un compte avant de publier une annonce")

            return redirect('login')

        ctx = {'services': Service.objects.all()}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):

        SERVICE = request.POST['service_type']

        categories = Categories.objects.filter(
            service__service_type__iexact=SERVICE)

        categories_str = []

        for categorie in categories:
            categories_str.append(categorie.categorie_name)

        return HttpResponse(json.dumps({'success': True, 'categories': categories_str}), content_type='application/json')


class Profile(LoginRequiredMixin, View):
    template_name = 'ss/profile.html'

    def get(self, request, *args, **kwargs):
        profileUpdateForm = forms.ProfileForm(
            instance=get_object_or_404(User, id=request.user.id))
        ctx = {'form': profileUpdateForm}

        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = forms.ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.biographie = form.cleaned_data["biographie"]
            user.tel_number = form.cleaned_data["tel_number"]
            if form.cleaned_data["profile_image"]:
                user.profile_image = form.cleaned_data["profile_image"]
            user.save()

            messages.info(request, "Votre profile a ete mise a jour")

            REDIRCT_TO = reverse('profile', args=[str(request.user.id)])

            return HttpResponse(
                json.dumps({'success': True, 'redirect_to': REDIRCT_TO}),
                content_type='application/json')

        profileUpdateForm = form_render(form, request)

        return HttpResponse(
            json.dumps(
                {'success': False, 'profileUpdateForm': profileUpdateForm}),
            content_type='application/json')


class CreateAnnonce(View):
    def post(self, request, *args, **kwargs):
        AnnonceModel.objects.create(
            categorie=request.POST["categorie"],
            title=request.POST["title"],
            description=request.POST["description"],
            user=request.user,
            annonce_image=request.FILES["annonce_image"])

        REDIRECT_TO = reverse('profile', args=[str(request.user.id)])
        return HttpResponse(
            json.dumps(
                {'success': True, 'redirect_to': REDIRECT_TO}),
            content_type="application/json")

    def get(self, request, *args, **kwargs):
        last_annonces = AnnonceModel.objects.all().order_by(
            '-publish_date')[:6]
        annonce_list = [
            {
                'id': annonce.id,
                'url': reverse('annonce-detail', kwargs={'id': annonce.id}),
                'categorie': annonce.categorie,
                'title': annonce.title,
                'description': annonce.description,
                'author_image': annonce.user.profile_image.url,
                'author_name': annonce.user.first_name,
                'author_last_name': annonce.user.last_name,
                'profile': reverse('profile', args=[str(annonce.user.id)]),
                'pub_date': '{0}/{1}/{2}'.format(annonce.publish_date.day, annonce.publish_date.month, annonce.publish_date.year),
                'annonce_image': annonce.annonce_image.url
            }
            for annonce in last_annonces
        ]

        return HttpResponse(
            json.dumps(
                {'success': True, 'annonce_list': annonce_list}),
            content_type="application/json")


class AnnonceDetail(DetailView):
    model = 'AnnonceModel'
    template_name = 'ss/detail.html'
    context_object_name = "annonce"

    def get_object(self):
        _id = self.kwargs.get('id')
        return get_object_or_404(AnnonceModel, id=_id)
