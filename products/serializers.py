from rest_framework import serializers

from .utils import StripeAPI

"""REPLACE WITH STRIPE API OR REMOVE"""
# class CreateProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = "__all__"

#     def validate_name(self, value):
#         if len(value) < 3:
#             raise serializers.ValidationError("Name to short.")
#         return value

#     def validate_price(self, value):
#         if value < 0:
#             raise serializers.ValidationError("Must be positive number.")
#         return value

#     def create(self, validated_data):
#         stripe_api = StripeAPI()
#         stripe_product = stripe_api.create_product_with_price_stripe(
#             validated_data["name"], validated_data["price"]
#         )
#         validated_data["stripe_product_id"] = stripe_product.product
#         validated_data["stripe_price_id"] = stripe_product.id
#         return Product.objects.create(**validated_data)
