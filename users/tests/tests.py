import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.db.models import Count

from products.models import Order

pytestmark = pytest.mark.django_db


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return "Bearer {0}".format(str(refresh.access_token))


class TestUserObtainToken:
    def test_fail_to_obtain_user_token(self, client, user_factory):
        user = user_factory()
        response = client.post(
            reverse("token_obtain_pair"),
            {"email": user.email, "password": "wrong_password"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_obtain_user_token(self, client, user_factory):
        user = user_factory()
        response = client.post(
            reverse("token_obtain_pair"),
            {"email": user.email, "password": user.plain_password},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK, response.data


class TestListUsers:
    def test_list_users_failed_authorization(self, client, user_factory):
        response = client.get(reverse("list_users"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_users_authorization(self, client, user_factory):
        user = user_factory()
        response = client.get(
            reverse("list_users"), HTTP_AUTHORIZATION=get_tokens_for_user(user)
        )

        assert response.status_code == status.HTTP_200_OK, response.data

    def test_list_users_company_details(self, client, company_user_factory):
        user = company_user_factory()
        response = client.get(
            reverse("list_users"), HTTP_AUTHORIZATION=get_tokens_for_user(user)
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["details"]["vat_id"]

    def test_list_users_user_details(self, client, user_factory):
        user = user_factory()
        response = client.get(
            reverse("list_users"), HTTP_AUTHORIZATION=get_tokens_for_user(user)
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["details"]["city"]
        assert response.data[0]["details"]["street"]

    def test_list_users_no_admins(self, client, admin_user_factory):
        user = admin_user_factory()
        response = client.get(
            reverse("list_users"), HTTP_AUTHORIZATION=get_tokens_for_user(user)
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_both_type_of_users_returned(
        self, client, user_factory, company_user_factory
    ):
        user = user_factory()
        user_2 = company_user_factory()
        response = client.get(
            reverse("list_users"), HTTP_AUTHORIZATION=get_tokens_for_user(user)
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["details"]["street"]
        assert response.data[0]["details"]["city"]
        assert response.data[1]["details"]["vat_id"]

    def test_create_checkout_session(
        self, client, user_factory, create_checkout_session_mock
    ):
        user = user_factory()
        response = client.post(
            reverse("stripe-checkout", args=(1,)),
            HTTP_AUTHORIZATION=get_tokens_for_user(user),
        )

        assert response.status_code == status.HTTP_302_FOUND
        assert response.headers["Location"] == "https://url.com"

    def test_create_order_webhook(
        self, client, user_factory, create_webhook_event_mock
    ):
        user = user_factory()
        response = client.post(reverse("stripe-webhook"))
        count = Order.objects.aggregate(Count("id"))

        assert response.status_code == status.HTTP_200_OK
        assert count["id__count"] == 1

    def test_created_order_data(self, client, user_factory, create_webhook_event_mock):
        user = user_factory()
        response = client.post(reverse("stripe-webhook"))
        order = Order.objects.get(id=1)

        assert response.status_code == status.HTTP_200_OK
        assert order.amount_total == 100
        assert order.product == "product"
        assert order.email == "email@email.com"

    def test_expired_checkout_webhook(
        self, client, user_factory, create_webhook_expired_event_mock
    ):
        user = user_factory()
        response = client.post(reverse("stripe-webhook"))
        count = Order.objects.aggregate(Count("id"))

        assert response.status_code == status.HTTP_200_OK
        assert count["id__count"] == 0