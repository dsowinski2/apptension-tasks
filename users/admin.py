from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.models import BaseInlineFormSet

from .models import User, UserDetails, CompanyDetails


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "username", "is_company")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "username",
            "is_active",
            "is_admin",
            "is_company",
        )

    def clean_password(self):
        return self.initial["password"]


class UserDetailsAdmin(admin.TabularInline):
    model = UserDetails


class CompanyDetailsAdmin(admin.TabularInline):
    model = CompanyDetails


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "username", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "is_company")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "is_company"),
            },
        ),
    )
    search_fields = ("email",)
    filter_horizontal = ()
    inlines = [
        UserDetailsAdmin,
        CompanyDetailsAdmin,
    ]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
