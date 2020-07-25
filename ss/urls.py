from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signin', views.LoginView.as_view(), name='login'),
    path('logout', views.log_out, name='logout'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('annonce', views.Annonce.as_view(), name='annonce'),
    path('create-annonce', views.CreateAnnonce.as_view(), name='create-annonce'),
    path('profile/<int:id>', views.Profile.as_view(), name='profile')
]
