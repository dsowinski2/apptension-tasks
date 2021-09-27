from urllib.parse import urljoin

from django.conf import settings
from rest_framework.exceptions import APIException
import stripe

from .error import ErrorHandler


class StripeAPI:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    def evaluate_stripe_response(self, stripe_response):
        if not len(stripe_response):
            raise APIException("No Data")

    def create_product_with_price_stripe(self, product_name, price):
        data = stripe.Price.create(
            unit_amount=price * 10, currency="eur", product_data={"name": product_name}
        )
        return data

    def list_products_stripe(self):
        try:
            products = stripe.Product.list()
            self.evaluate_stripe_response(products)
            return products["data"]
        except Exception as e:
            ErrorHandler().create_error(e)

    def list_prices_stripe(self):
        try:
            prices = stripe.Price.list()
            self.evaluate_stripe_response(prices)
            return prices["data"]
        except Exception as e:
            ErrorHandler().create_error(e)

    def combine_product_with_price(self):
        prices = self.list_prices_stripe()
        products = self.list_products_stripe()
        index_table = {
            key.product: index for index, key in zip(range(len(prices)), prices)
        }
        for product in products:
            if product.id in index_table.keys():
                product["price"] = {
                    "price": prices[index_table[product.id]]["unit_amount"],
                    "price_id": prices[index_table[product.id]]["id"],
                }
        return products

    def get_product_with_price_stripe(self, price_id):
        price = stripe.Price.retrieve(price_id)
        product = price["product"]
        return product

    def create_checkout_session_stripe(self, price_id, user):
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                },
            ],
            payment_method_types=[
                "card",
                "p24",
            ],
            mode="payment",
            success_url=urljoin(settings.BASE_URL + "/users/stripe/success/"),
            cancel_url=urljoin(settings.BASE_URL, "/users/stripe/cancel/"),
            metadata={
                "user_id": user,
                "product": self.get_product_with_price_stripe(price_id),
            },
        )
        return checkout_session

    def create_webhook_event_stripe(self, request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

        event = stripe.Webhook.construct_event(
            payload, sig_header, self.endpoint_secret
        )
        return event