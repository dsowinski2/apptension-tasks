import pytest
import pytest_factoryboy

from users.tests import factories as user_factories

pytest_factoryboy.register(user_factories.UserFactory)
pytest_factoryboy.register(user_factories.CompanyUserFactory)
pytest_factoryboy.register(user_factories.UserDetailsFactory)
pytest_factoryboy.register(user_factories.CompanyDetailsFactory)
pytest_factoryboy.register(user_factories.AdminUserFactory)


@pytest.fixture()
def create_checkout_session_mock(mocker):
    class MockResponse:
        def __init__(self, url):
            self.url = url

    return mocker.patch(
        "products.utils.StripeAPI.create_checkout_session_stripe",
        return_value=MockResponse("https://url.com"),
    )


@pytest.fixture()
def create_webhook_event_mock(mocker):
    return mocker.patch(
        "products.utils.StripeAPI.create_webhook_event_stripe",
        return_value={
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "amount_total": 100,
                    "customer_details": {"email": "email@email.com"},
                    "metadata": {"user_id": 1, "product": "product"},
                    "payment_status": "paid",
                }
            },
        },
    )


@pytest.fixture()
def create_webhook_expired_event_mock(mocker):
    return mocker.patch(
        "products.utils.StripeAPI.create_webhook_event_stripe",
        return_value={
            "type": "checkout.session.expired",
            "data": {
                "object": {
                    "amount_total": 100,
                    "customer_details": {"email": "email@email.com"},
                    "metadata": {"user_id": 1, "product": "product"},
                    "payment_status": "paid",
                }
            },
        },
    )
