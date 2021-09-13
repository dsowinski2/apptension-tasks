from rest_framework import serializers

from .models import User, UserDetails, CompanyDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "is_company", "details"]

    details = serializers.SerializerMethodField("get_data")

    def get_data(self, instance):
        if instance.is_company:
            details = instance.companydetails
            return CompanyDetailsSerializer(details).data
        details = instance.userdetails
        return UserDetailsSerializer(details).data


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ["city", "street"]


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ["vat_id"]
