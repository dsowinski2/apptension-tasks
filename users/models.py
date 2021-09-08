# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import UserManager

# class User(AbstractUser):
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     email = models.EmailField(unique=True)
#     username = models.TextField(default=None)
#     is_company = models.BooleanField(default=False)
#     # user_details_id = models.OneToOneField(UserDetails, blank=True, default=None, null=True, on_delete=models.CASCADE)
#     # company_details_id = models.OneToOneField(CompanyDetails, blank=True, default=None, null=True, on_delete=models.CASCADE,)	
    
# class UserDetails(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, primary_key=True)
# 	city = models.TextField()
# 	street = models.TextField()

# class CompanyDetails(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, primary_key=True)
# 	vat_id = models.TextField()


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

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
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.TextField(default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, primary_key=True)
	city = models.TextField()
	street = models.TextField()

class CompanyDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default=None, primary_key=True)
	vat_id = models.TextField()