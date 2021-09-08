import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

from .. models import User

class TestUserObtainToken:
	def test_fail_to_obtain_user_token(self, client, user_factory):
		user = user_factory.create()
		response = client.post(reverse('token_obtain_pair'), {"email": user.email, "password": "wrong_password"}, format='json')
		assert response.status_code == 401

	def test_obtain_user_token(self, client, user_factory):
		user = user_factory.create()
		response = client.post(reverse('token_obtain_pair'), {"email": user.email, "password": user.plain_password}, format='json')
		assert response.status_code == 200, response.data

class TestListUsers:
	def test_list_users_authorization(self, client, user_factory):
		user = user_factory.create()
		data = {"email": user.email, "password": user.plain_password}
		token = client.post(reverse('token_obtain_pair'), data=data).data['access']
		jwt = 'Bearer {0}'.format(token)
		response = client.get(reverse('list_users'), HTTP_AUTHORIZATION=jwt)

		assert response.status_code == 200, response.data

	# def test_list_users_user_details
	# create more factors
	# def test_list_users_company_details
	# create more factors
	# def test_list_users_no_admins
	#filter users in View

	 