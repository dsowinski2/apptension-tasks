import stripe
from django.conf import settings


class StripeAPI:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    def create_product_with_price_stripe(self, product_name, price):
        price = price * 10
        data = stripe.Price.create(
            unit_amount=price, currency="eur", product_data={"name": product_name}
        )
        return data

    def list_products_stripe(self):
        products = stripe.Product.list()
        return products["data"]

    def list_prices_stripe(self):
        prices = stripe.Price.list()
        return prices["data"]

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
            success_url="http://127.0.0.1:8000" + "/users/stripe/success/",
            cancel_url="http://127.0.0.1:8000" + "/users/stripe/cancel/",
            metadata={
                "user_id": user,
                "product": self.get_product_with_price_stripe(price_id),
            },
        )
        return checkout_session

    def create_webhook_event_stripe(self, request):
        payload = request.body
        sig_header = None
        if "HTTP_STRIPE_SIGNATURE" in request.META:
            sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
            
        event = stripe.Webhook.construct_event(
            payload, sig_header, self.endpoint_secret
        )
        return event
