from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from django.conf import settings
from rest_framework.exceptions import APIException
from .utils import StripeAPI


class ListStripeProductsView(APIView):
    def get(self, request):
        stripe_api = StripeAPI()
        products = stripe_api.combine_product_with_price()
        return Response(products)
