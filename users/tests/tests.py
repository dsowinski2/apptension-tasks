import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

pytestmark = pytest.mark.django_db



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return 'Bearer {0}'.format(str(refresh.access_token))


class TestUserObtainToken:
	def test_fail_to_obtain_user_token(self, client, user_factory):
		user = user_factory()
		response = client.post(reverse('token_obtain_pair'), {"email": user.email, "password": "wrong_password"}, format='json')
		
		assert response.status_code == status.HTTP_401_UNAUTHORIZED

	def test_obtain_user_token(self, client, user_factory):
		user = user_factory()
		response = client.post(reverse('token_obtain_pair'), {"email": user.email, "password": user.plain_password}, format='json')
		
		assert response.status_code == status.HTTP_200_OK, response.data

class TestListUsers:
	def test_list_users_failed_authorization(self, client, user_factory):
		response = client.get(reverse('list_users'))

		assert response.status_code == status.HTTP_401_UNAUTHORIZED

	def test_list_users_authorization(self, client, user_factory):
		user = user_factory()
		response = client.get(reverse('list_users'), HTTP_AUTHORIZATION=get_tokens_for_user(user))

		assert response.status_code == status.HTTP_200_OK, response.data

	def test_list_users_company_details(self, client, company_user_factory):
		user = company_user_factory()
		response = client.get(reverse('list_users'), HTTP_AUTHORIZATION=get_tokens_for_user(user))
		
		assert response.status_code == status.HTTP_200_OK
		assert response.data[0]['details']['vat_id']

	def test_list_users_user_details(self, client, user_factory):
		user = user_factory()
		response = client.get(reverse('list_users'), HTTP_AUTHORIZATION=get_tokens_for_user(user))
		
		assert response.status_code == status.HTTP_200_OK
		assert response.data[0]['details']['city']
		assert response.data[0]['details']['street']

	def test_list_users_no_admins(self, client, admin_user_factory):
		user = admin_user_factory()
		response = client.get(reverse('list_users'), HTTP_AUTHORIZATION=get_tokens_for_user(user))

		assert response.status_code == status.HTTP_200_OK
		assert len(response.data) == 0

	def test_both_type_of_users_returned(self, client, user_factory, company_user_factory):
		user = user_factory()
		user_2 = company_user_factory()
		response = client.get(reverse('list_users'), HTTP_AUTHORIZATION=get_tokens_for_user(user))

		assert response.status_code == status.HTTP_200_OK
		assert len(response.data) == 2
		assert response.data[0]['details']['street']
		assert response.data[0]['details']['city']
		assert response.data[1]['details']['vat_id']
		

	 