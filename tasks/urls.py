"""tasks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views
from users import views as user_views
from products import views as product_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("users/", user_views.ListUsers.as_view(), name="list_users"),
    path(
        "users/stripe/checkout/<str:pk>/",
        user_views.StripeCheckoutView.as_view(),
        name="stripe-checkout",
    ),
    path(
        "users/stripe/success/",
        user_views.SuccessedCheckoutView.as_view(),
        name="successed-checkout",
    ),
    path(
        "users/stripe/cancel/",
        user_views.CancelledCheckoutView.as_view(),
        name="cancelled-checkout",
    ),
    path(
        "users/stripe/webhook/",
        user_views.StripeWebhooksView.as_view(),
        name="stripe-webhook",
    ),
    path("users/stripe/", user_views.CheckoutView.as_view(), name="checkout"),
    path(
        "users/stripe/products/",
        product_views.ListStripeProductsView.as_view(),
        name="list-products",
    ),
]
# + static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, '/static'))
