from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .serializers import UserSerializer
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
        print(checkout_session)
        return redirect(checkout_session.url, code=303)


class SuccessedCheckoutView(TemplateView):
    template_name = "success_payment.html"


class CheckoutView(TemplateView):
    template_name = "checkout.html"


class CancelledCheckoutView(TemplateView):
    template_name = "cancelled_payment.html"


class StripeWebhooksView(APIView):
    endpoint_secret = "whsec_Pk9ZEDdBzCoCp1XoqDSKSZiHMq7RM2TD"

    def post(self, request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.endpoint_secret
            )
        except ValueError as e:
            """Invalid payload"""
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            """Invalid signature"""
            return HttpResponse(status=400)
        print(event)
        return Response(status=200)
