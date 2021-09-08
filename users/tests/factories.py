import factory

from django.contrib.auth import hashers

from .. models import User

class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
	email = 'email@email.com'
	username = 'username'
	password = 'password'
	is_active = True
	is_admin = True
	is_company = True

	@classmethod
	def _create(cls, *args, **kwargs):
		plain_password = kwargs.pop("password", "password")
		password = hashers.make_password(plain_password)
		user = super()._create(*args, **kwargs, password=password)
		setattr(user, "plain_password", plain_password)
		return user
