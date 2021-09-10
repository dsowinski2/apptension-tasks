from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from .models import User

class ListUsers(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = UserSerializer
	def get_queryset(self):
		users = User.objects.filter(is_admin=False).select_related('userdetails', 'companydetails')
		return users

	def get(self, request):
		users = self.get_queryset()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)

