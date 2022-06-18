from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ("username", "email", "first_name", "last_name", "is_staff", "age", "background")

    add_fieldsets = UserAdmin.add_fieldsets + (("Additional fields", {"fields": ("age", "background")}))
    fieldsets = UserAdmin.fieldsets + (("Additional fields", {"fields": ("age",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
