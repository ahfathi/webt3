from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'nickname', 'email', 'avatar']
    add_fieldsets = (
        (None, {'fields': ('username', 'nickname', 'password1', 'password2')}),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('nickname', 'email', 'avatar')}),
        UserAdmin.fieldsets[2],
    )

admin.site.register(User, CustomUserAdmin)