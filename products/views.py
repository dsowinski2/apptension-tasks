from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
import stripe

from .utils import StripeAPI


class ListStripeProductsView(APIView):
    def get(self, request):
        products = StripeAPI().combine_product_with_price()
        return Response(products)
