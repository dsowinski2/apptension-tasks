from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from django.conf import settings
from rest_framework.exceptions import APIException
from .utils import StripeAPI

"""Replace this View with adding products with stripe API or remove"""

# class AddProductView(APIView):
#     def get_queryset(self, name):
#         products = Product.objects.filter(name=name)
#         return products

#     def post(self, request, *args, **kwargs):
#         name = request.data["name"]

#         products = self.get_queryset(name)
#         if products:
#             raise APIException("Product with provided title already exists!")
#         serializer = CreateProductSerializer(data=request.data)
#         if not serializer.is_valid():
#             print(serializer.errors)
#             return Response(serializer.errors)
#         print(serializer)
#         serializer.save()
#         return Response(serializer.data)


class ListStripeProductsView(APIView):
    def get(self, request):
        stripe_api = StripeAPI()
        products = stripe_api.combine_product_with_price()
        return Response(products)
