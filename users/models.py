from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), username=username)

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ACCOUNT_TYPE_CHOICES = [
        ("FREE", "FREE"),
        ("PREMIUM", "PREMIUM"),
    ]

    email = models.EmailField(max_length=255, unique=True)
    username = models.TextField(max_length=255, default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    account_type = models.CharField(
        max_length=10, choices=ACCOUNT_TYPE_CHOICES, null=False
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def set_account_type(self):
        if self.is_admin and self.is_company:
            return "PREMIUM"
        else:
            return "FREE"

    @property
    def is_staff(self):
        return self.is_admin


class UserDetails(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, default=None, primary_key=True
    )
    city = models.TextField(max_length=255)
    street = models.TextField(max_length=255)


class CompanyDetails(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, default=None, primary_key=True
    )
    vat_id = models.TextField(max_length=255)
