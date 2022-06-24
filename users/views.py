from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .serializers import UserSerializer, CreateOrderSerializer
from .models import User

from products.utils import StripeAPI


class ListUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        users = User.objects.filter(is_admin=False).select_related(
            "userdetails", "companydetails"
        )
        return users

    def get(self, request):
        users = self.get_queryset()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class StripeCheckoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        stripe_api = StripeAPI()
        checkout_session = stripe_api.create_checkout_session_stripe(
            pk, request.user.id
        )
        return redirect(checkout_session.url, code=303)


class SuccessedCheckoutView(TemplateView):
    template_name = "success_payment.html"


class CheckoutView(TemplateView):
    template_name = "checkout.html"


class CancelledCheckoutView(TemplateView):
    template_name = "cancelled_payment.html"


class StripeWebhooksView(APIView):
    def post(self, request):

        event = None
        try:
            stripe_api = StripeAPI()
            event = stripe_api.create_webhook_event_stripe(request)
        except ValueError as e:
            return Response(status=400)

        except stripe.error.SignatureVerificationError as e:
            return Response(status=400)
            
        if event["type"] == "checkout.session.completed":
            webhook_data = event["data"]["object"]
            data = {
                "amount_total": webhook_data["amount_total"],
                "email": webhook_data["customer_details"]["email"],
                "user": webhook_data["metadata"]["user_id"],
                "product": webhook_data["metadata"]["product"],
                "payment_status": webhook_data["payment_status"],
            }
            serializer = CreateOrderSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors)
            serializer.save()

        return Response(status=200)
