from django.apps import apps

from rest_framework import serializers

from .models import User, UserDetails, CompanyDetails

class UserSerializer(serializers.ModelSerializer):

	class Meta: 
		model = User
		fields = ['email', 'username', 'is_company', 'details']

	details = serializers.SerializerMethodField('get_data')

	def get_data(self, instance):
		# print(instance)
		if instance.is_company:
			data = CompanyDetails.objects.filter(pk=instance.id)
			# data = instance.select_related('CompanyDetails')
			return CompanyDetailsSerializer(data, many=True).data
		data = UserDetails.objects.filter(pk=instance.id)
		return UserDetailsSerializer(data, many=True).data

class UserDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserDetails
		fields = ['city', 'street']

class CompanyDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompanyDetails
		fields = ['vat_id']

