from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .forms import UserCreationForm, UserChangeForm, SignupForm
from .models import User, AnnonceModel, Service, Categories, Notification, Interet


admin.site.register(AnnonceModel)
admin.site.register(Notification)
admin.site.register(Categories)
admin.site.register(Interet)


class CategorieInline(admin.TabularInline):
    '''Tabular Inline View for Categorie'''

    model = Categories


@admin.register(Service)
class Admin(admin.ModelAdmin):
    '''Admin View for '''
    inlines = [
        CategorieInline,
    ]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    form = UserChangeForm
    model = User

    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'password1')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
