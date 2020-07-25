from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import login,  authenticate, logout
from . import forms
from django.template.context_processors import csrf
import json
from django.http import HttpResponse
from crispy_forms.utils import render_crispy_form
from .models import User
from django.views.generic.edit import (UpdateView)
from django.contrib import messages
from .models import Service, Categories, Annonce
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

        username = request.POST.get('email')
        raw_password = request.POST.get('password1')
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

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


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
            print(username)
            user = authenticate(username=username, password=raw_password)

            if user is not None:
                login(request, user)
                messages.success(request, "Votre Compte est cree avec success")

            return HttpResponse(json.dumps({'success': True, 'redirect_url': '/', }), content_type='application/json')

        signupForm = form_render(form, request)

        return HttpResponse(json.dumps({'success': False, 'form_html': signupForm}), content_type='application/json')


class Annonce(View):
    template_name = "ss/annonce.html"

    def get(self, request):
        print("hello")
        if not request.user.is_authenticated:
            messages.info(
                request, "Vous devez avoir un compte avant de publier une annonce")
            return redirect('login')

        ctx = {'services': Service.objects.all()}
        return render(request, self.template_name, ctx)

    def post(self, request):
        SERVICE = request.POST['service_type']
        categories = Categories.objects.filter(
            service__service_type__iexact=SERVICE)
        categories_str = []
        for categorie in categories:
            categories_str.append(categorie.categorie_name)
        return HttpResponse(json.dumps({'success': True, 'categories': categories_str}), content_type='application/json')


class CreateAnnonce(View):
    def post(self, request):
        pass


class Profile(LoginRequiredMixin, View):
    template_name = 'ss/profile.html'

    def get(self, request, *args, **kwargs):
        profileUpdateForm = forms.ProfileForm(
            instance=get_object_or_404(User, id=request.user.id))
        ctx = {'form': profileUpdateForm}

        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = forms.ProfileForm(data=request.POST)

        if form.is_valid():
            c_user = User.objects.get(id=request.user.id)
            c_user.first_name = request.POST['first_name']
            c_user.last_name = request.POST['last_name']
            c_user.description = request.POST['description']
            c_user.tel_number = request.POST['tel_number']
            c_user.save()

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
