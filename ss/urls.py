from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signin', views.LoginView.as_view(), name='login'),
    path('logout', views.log_out, name='logout'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('annonce', views.Annonce.as_view(), name='annonce'),
    path('create-annonce', views.CreateAnnonce.as_view(), name='create-annonce'),
    path('profile/<int:id>', views.Profile.as_view(), name='profile'),
    path('annonce/<int:id>', views.AnnonceDetail.as_view(), name='annonce-detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
