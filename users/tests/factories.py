import factory
from django.contrib.auth import hashers

from .. models import User, UserDetails, CompanyDetails

class UserDetailsFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = UserDetails
		
	user = factory.SubFactory('users.tests.factories.UserFactory')	
	city = 'Poznan'
	street = 'Nowowiejskiego'

class CompanyDetailsFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = CompanyDetails
		
	user = factory.SubFactory('users.tests.factories.CompanyUserFactory')
	vat_id = 123

class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	email = 'email@email.com'
	username = 'username'
	password = 'password'
	is_active = True
	is_admin = False
	is_company = False
	details = factory.RelatedFactory(UserDetailsFactory, factory_related_name='user')

	@classmethod
	def _create(cls, *args, **kwargs):
		plain_password = kwargs.pop("password", "password")
		password = hashers.make_password(plain_password)
		user = super()._create(*args, **kwargs, password=password)
		setattr(user, "plain_password", plain_password)
		return user

class CompanyUserFactory(UserFactory):
	class Meta:
		model = User

	is_company = True
	details = factory.RelatedFactory(CompanyDetailsFactory, factory_related_name='user')

class AdminUserFactory(UserFactory):
	class Meta:
		model = User
		
	is_admin = True